from __future__ import annotations

from typing import Any
import pyarrow.parquet as pq
import pandas as pd
import pyarrow.compute as pc
from dojo.datasource.config import HFConfig
from dojo.datasource.registry import HFEndpointSpec, resolve
from dojo._exceptions import OfflineDataNotAvailableError
from dojo.logging import logger
import ctypes
import threading
import time


class DownloadStalledError(Exception):
    pass


def _async_raise(tid, exctype):
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
    if res == 0:
        pass
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)


_active_downloads = {}
_active_downloads_lock = threading.Lock()


try:
    import huggingface_hub.utils._progress

    original_tqdm = huggingface_hub.utils._progress.tqdm

    class WatchdogTqdm(original_tqdm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._tid = threading.get_ident()
            with _active_downloads_lock:
                _active_downloads[self._tid] = {"last_update_time": time.time(), "last_n": getattr(self, "n", 0)}

        def update(self, n=1):
            super().update(n)
            with _active_downloads_lock:
                if self._tid in _active_downloads:
                    if getattr(self, "n", 0) > _active_downloads[self._tid].get("last_n", 0):
                        _active_downloads[self._tid]["last_n"] = getattr(self, "n", 0)
                        _active_downloads[self._tid]["last_update_time"] = time.time()

        def close(self):
            super().close()
            with _active_downloads_lock:
                if self._tid in _active_downloads:
                    del _active_downloads[self._tid]

    huggingface_hub.utils._progress.tqdm = WatchdogTqdm
except ImportError:
    pass

# try:
#     import modelscope.hub.file_download
#     original_ms_tqdm = modelscope.hub.file_download.tqdm

#     class WatchdogTqdmMS(original_ms_tqdm):
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             self._tid = threading.get_ident()
#             with _active_downloads_lock:
#                 _active_downloads[self._tid] = {"last_update_time": time.time(), "last_n": getattr(self, "n", 0)}

#         def update(self, n=1):
#             super().update(n)
#             with _active_downloads_lock:
#                 if self._tid in _active_downloads:
#                     if getattr(self, "n", 0) > _active_downloads[self._tid].get("last_n", 0):
#                         _active_downloads[self._tid]["last_n"] = getattr(self, "n", 0)
#                         _active_downloads[self._tid]["last_update_time"] = time.time()

#         def close(self):
#             super().close()
#             with _active_downloads_lock:
#                 if self._tid in _active_downloads:
#                     del _active_downloads[self._tid]

#     modelscope.hub.file_download.tqdm = WatchdogTqdmMS
# except Exception:
#     pass

_watchdog_started = False
_watchdog_start_lock = threading.Lock()


def _download_watchdog_loop():
    while True:
        time.sleep(1)
        now = time.time()
        with _active_downloads_lock:
            for tid, info in list(_active_downloads.items()):
                if now - info["last_update_time"] > 10:
                    _async_raise(tid, DownloadStalledError)
                    del _active_downloads[tid]


def _start_watchdog():
    global _watchdog_started
    with _watchdog_start_lock:
        if not _watchdog_started:
            t = threading.Thread(target=_download_watchdog_loop, daemon=True, name="DojoSDK-DownloadWatchdog")
            t.start()
            _watchdog_started = True


class HuggingFaceDataSource:
    _table_cache: dict[str, Any] = {}
    _df_cache: dict[str, Any] = {}

    def __init__(self, config: HFConfig | None = None) -> None:
        import threading

        self._cfg = config or HFConfig.from_env()
        self._bg_thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._cleanup_lock = threading.Lock()
        _start_watchdog()

    def fetch(self, *, method: str, path: str, params: dict[str, Any], json: Any | None = None) -> Any:
        spec = resolve(path)
        if spec is None:
            raise OfflineDataNotAvailableError(f"Endpoint {path} is not registered in the HuggingFace offline registry.")

        # Merge body into params for endpoints that might send filters in body
        merged = dict(params)
        if isinstance(json, dict):
            merged.update(json)

        table = self._load_dataset(spec, merged)
        rows = self._apply_filters(table, spec, merged)

        data: Any = {"total_num": len(rows), "data": rows} if spec.envelope == "list" else (rows[0] if rows else {})
        return {"code": 0, "message": "ok", "data": data}

    def fetch_df(self, *, path: str, params: dict[str, Any] | None = None, refresh: bool = False) -> Any:
        params = params or {}
        spec = resolve(path)
        if spec is None:
            raise OfflineDataNotAvailableError(f"Endpoint {path} is not registered in the HuggingFace offline registry.")

        relative = self._render_template(spec.path_template, params)
        cache_key = f"{spec.repo_id}/{relative}"

        if cache_key in self._df_cache and not refresh:
            return self._df_cache[cache_key]

        local_path = self._download_and_cleanup(
            repo_id=spec.repo_id,
            ms_repo_id=spec.ms_repo_id,
            filename=relative,
            repo_type="dataset",
            token=self._cfg.token,
            revision=self._cfg.revision,
        )

        df = pd.read_parquet(local_path)
        if "symbol" in df.columns and "bar_time" in df.columns:
            df = df.sort_values(by=["symbol", "bar_time"])
            df["index_symbol"] = df.symbol
            df = df.set_index("index_symbol")
        self._df_cache[cache_key] = df
        return df

    def _load_dataset(self, spec: HFEndpointSpec, params: dict[str, Any], refresh: bool = False):
        relative = self._render_template(spec.path_template, params)
        cache_key = f"{spec.repo_id}/{relative}"

        if cache_key in self._table_cache and not refresh:
            self._warm_companion_files(spec, params)
            return self._table_cache[cache_key]

        try:
            local_path = self._download_and_cleanup(
                repo_id=spec.repo_id,
                ms_repo_id=spec.ms_repo_id,
                filename=relative,
                repo_type="dataset",
                token=self._cfg.token,
                revision=self._cfg.revision,
                cache_dir=self._cfg.cache_dir,
                local_files_only=self._cfg.local_only,
            )
            table = pq.read_table(local_path)
            self._table_cache[cache_key] = table
            self._warm_companion_files(spec, params)
            return table
        except Exception as err:
            if spec.fallback_template:
                fb = self._render_template(spec.fallback_template, params)
                cache_key_fb = f"{spec.repo_id}/{fb}"

                if cache_key_fb in self._table_cache:
                    return self._table_cache[cache_key_fb]

                logger.warning(f"Failed to fetch main file {relative}, falling back to {fb}: {err}")
                try:
                    local_path = self._download_and_cleanup(
                        repo_id=spec.repo_id,
                        ms_repo_id=spec.ms_repo_id,
                        filename=fb,
                        repo_type="dataset",
                        token=self._cfg.token,
                        revision=self._cfg.revision,
                        cache_dir=self._cfg.cache_dir,
                        local_files_only=self._cfg.local_only,
                    )
                    table = pq.read_table(local_path)
                    self._table_cache[cache_key_fb] = table
                    self._warm_companion_files(spec, params)
                    return table
                except Exception as fb_err:
                    raise OfflineDataNotAvailableError(f"Cannot fetch offline file {spec.repo_id}/{fb}: {fb_err}") from fb_err
            raise OfflineDataNotAvailableError(f"Cannot fetch offline file {spec.repo_id}/{relative}: {err}") from err

    def _warm_companion_files(self, spec: HFEndpointSpec, params: dict[str, Any]) -> None:
        for template in spec.companion_files:
            try:
                self._load_companion_dataset(spec.repo_id, template, params, spec.ms_repo_id)
            except Exception as err:
                logger.warning(f"Failed to warm companion file {spec.repo_id}/{template}: {err}")

    def _load_companion_dataset(self, repo_id: str, template: str, params: dict[str, Any], ms_repo_id: str | None = None):
        relative = self._render_template(template, params)
        cache_key = f"{repo_id}/{relative}"
        if cache_key in self._table_cache:
            return self._table_cache[cache_key]

        local_path = self._download_and_cleanup(
            repo_id=repo_id,
            ms_repo_id=ms_repo_id or repo_id,
            filename=relative,
            repo_type="dataset",
            token=self._cfg.token,
            revision=self._cfg.revision,
            cache_dir=self._cfg.cache_dir,
            local_files_only=self._cfg.local_only,
        )
        table = pq.read_table(local_path)
        self._table_cache[cache_key] = table
        return table

    @staticmethod
    def _render_template(template: str, params: dict[str, Any]) -> str:
        try:
            return template.format(**params)
        except KeyError as e:
            raise OfflineDataNotAvailableError(f"Offline file path template {template!r} is missing required parameter {e}") from e

    def _download_and_cleanup(self, **kwargs) -> str:
        from huggingface_hub import hf_hub_download
        from dojo.datasource.network import resolve_backend
        import os
        import threading
        import time

        tid = threading.get_ident()
        repo_id = kwargs.get("repo_id")
        ms_repo_id = kwargs.pop("ms_repo_id", repo_id)
        filename = kwargs.get("filename")

        backend = resolve_backend(self._cfg)

        while True:
            try:
                if backend == "huggingface":
                    with _active_downloads_lock:
                        _active_downloads[tid] = {"last_update_time": time.time(), "last_n": 0}

                if backend == "modelscope":
                    from modelscope.hub.file_download import dataset_file_download
                    from modelscope.hub.api import HubApi

                    api = HubApi()
                    if self._cfg.modelscope_token:
                        api.login(self._cfg.modelscope_token)

                    ms_revision = kwargs.get("revision", "master")
                    if ms_revision == "main":
                        ms_revision = "master"

                    local_files_only = kwargs.get("local_files_only", False)
                    if not local_files_only:
                        try:
                            files = api.get_dataset_files(ms_repo_id, revision=ms_revision)
                            for f in files:
                                if f.get("Path") == filename and f.get("Revision"):
                                    ms_revision = f["Revision"]
                                    break
                        except Exception as e:
                            logger.debug(f"Failed to fetch dataset files for {ms_repo_id}: {e}")
                    local_path = dataset_file_download(
                        dataset_id=ms_repo_id, file_path=filename, revision=ms_revision, token=self._cfg.modelscope_token, local_files_only=kwargs.get("local_files_only", False)
                    )
                else:
                    local_path = hf_hub_download(**kwargs)
                break
            except DownloadStalledError:
                logger.warning(f"Download for {repo_id}/{filename} stalled for >10s. Restarting {backend} download...")
                time.sleep(1)
            finally:
                if backend == "huggingface":
                    with _active_downloads_lock:
                        if tid in _active_downloads:
                            del _active_downloads[tid]

        if not repo_id:
            return local_path

        try:
            parts = local_path.split(os.sep)
            if "snapshots" in parts:
                snapshots_idx = parts.index("snapshots")
                commit_hash = parts[snapshots_idx + 1]
                repo_dir = os.sep.join(parts[:snapshots_idx])
                snapshots_dir = os.path.join(repo_dir, "snapshots")

                if os.path.exists(snapshots_dir):
                    snapshots = [d for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))]
                    if len(snapshots) > 1:
                        with self._cleanup_lock:
                            snapshots = [d for d in os.listdir(snapshots_dir) if os.path.isdir(os.path.join(snapshots_dir, d))]
                            other_commits = [s for s in snapshots if s != commit_hash]
                            if other_commits:
                                if backend == "huggingface":
                                    from huggingface_hub import scan_cache_dir

                                    cache_info = scan_cache_dir(self._cfg.cache_dir)
                                    for repo in cache_info.repos:
                                        if repo.repo_id == repo_id:
                                            strategy = cache_info.delete_revisions(*other_commits)
                                            if strategy.expected_freed_size > 0:
                                                strategy.execute()
                                                logger.info(f"Cleaned up old huggingface revisions for {repo_id}: {other_commits}")
                                elif backend == "modelscope":
                                    import shutil

                                    for c in other_commits:
                                        path_to_delete = os.path.join(snapshots_dir, c)
                                        shutil.rmtree(path_to_delete, ignore_errors=True)
                                    logger.debug(f"Cleaned up old modelscope revisions for {ms_repo_id}: {other_commits}")
        except Exception as e:
            logger.warning(f"Failed to perform cache cleanup for {repo_id}: {e}")

        return local_path

    def _apply_filters(self, table, spec: HFEndpointSpec, params: dict[str, Any]) -> list[dict]:
        mask = None

        if spec.symbol_field and spec.symbol_param in params:
            val = params[spec.symbol_param]
            if isinstance(val, str) and "," in val:
                val = val.split(",")

            if isinstance(val, (list, tuple, set)):
                import pyarrow as pa

                cond = pc.is_in(table[spec.symbol_field], value_set=pa.array(list(val)))
            else:
                cond = pc.equal(table[spec.symbol_field], val)
            mask = cond if mask is None else pc.and_(mask, cond)

        # Generic filtering: any param key that matches a column name is applied as an exact match filter
        ignore_params = {
            spec.limit_param,
            spec.start_param,
            spec.end_param,
            spec.fields_param,
        }
        if spec.symbol_field and spec.symbol_field != spec.symbol_param:
            ignore_params.add(spec.symbol_param)

        import pyarrow as pa

        for k, v in params.items():
            if k in ignore_params or v is None:
                continue
            if isinstance(v, dict):
                continue
            if isinstance(v, (list, tuple, set)) and any(isinstance(item, dict) for item in v):
                continue
            if k in table.column_names:
                # If value is a collection (e.g. list of markets), use is_in, else equal
                if isinstance(v, (list, tuple, set)):
                    cond = pc.is_in(table[k], value_set=pa.array(list(v)))
                else:
                    cond = pc.equal(table[k], v)
                mask = cond if mask is None else pc.and_(mask, cond)

        if spec.time_field and spec.time_field in table.column_names:
            col = table[spec.time_field]
            if params.get(spec.start_param) is not None:
                cond = pc.greater_equal(col, params[spec.start_param])
                mask = cond if mask is None else pc.and_(mask, cond)
            if params.get(spec.end_param) is not None:
                cond = pc.less_equal(col, params[spec.end_param])
                mask = cond if mask is None else pc.and_(mask, cond)

        if mask is not None:
            table = table.filter(mask)

        if spec.time_field and spec.time_field in table.column_names:
            table = table.sort_by([(spec.time_field, "descending" if spec.order_desc else "ascending")])

        limit = params.get(spec.limit_param)
        if isinstance(limit, int) and limit > 0:
            table = table.slice(0, limit)

        rows = table.to_pylist()

        # [NEW] Check metadata for json columns and deserialize
        json_cols = []
        if spec.json_columns:
            json_cols = spec.json_columns
        else:
            metadata = table.schema.metadata
            if metadata and b"dojosdk:json_columns" in metadata:
                json_cols = metadata[b"dojosdk:json_columns"].decode("utf-8").split(",")

        if json_cols:
            import json

            json_cols_set = set(json_cols)
            for row in rows:
                for col in json_cols_set:
                    val = row.get(col)
                    if isinstance(val, str):
                        try:
                            row[col] = json.loads(val)
                        except json.JSONDecodeError:
                            pass

        if spec.fields_param and params.get(spec.fields_param):
            keep = set(params[spec.fields_param])
            rows = [{k: v for k, v in r.items() if k in keep} for r in rows]

        import datetime

        for row in rows:
            for k, v in row.items():
                if isinstance(v, (datetime.datetime, datetime.date)):
                    row[k] = v.isoformat()

        return rows

    def refresh_all_caches(self) -> None:
        """Force redownload and recache all registered endpoints."""
        from dojo.datasource.registry import HF_REGISTRY

        logger.info("Starting background refresh of all offline datasets...")
        for path, spec in HF_REGISTRY.items():
            if self._stop_event.is_set():
                break

            try:
                relative = self._render_template(spec.path_template, {})
            except Exception:
                continue

            cache_key = f"{spec.repo_id}/{relative}"
            try:
                local_path = self._download_and_cleanup(
                    repo_id=spec.repo_id,
                    ms_repo_id=spec.ms_repo_id,
                    filename=relative,
                    repo_type="dataset",
                    token=self._cfg.token,
                    revision=self._cfg.revision,
                    cache_dir=self._cfg.cache_dir,
                    force_download=True,
                )
                self._table_cache[cache_key] = pq.read_table(local_path)
                self._warm_companion_files(spec, {})
                logger.info(f"Successfully refreshed {cache_key}")
            except Exception as e:
                logger.warning(f"Failed to background refresh {cache_key}: {e}")
        logger.info("Background refresh complete.")

    def start_background_sync(self, interval_days: int = 1) -> None:
        """Start a daemon thread to refresh datasets periodically."""
        import threading

        if self._bg_thread is not None and self._bg_thread.is_alive():
            logger.info("Background sync is already running.")
            return

        self._stop_event.clear()

        def _sync_loop():
            while not self._stop_event.is_set():
                sleep_seconds = interval_days * 86400
                if self._stop_event.wait(sleep_seconds):
                    break

                if not self._cfg.local_only:
                    self.refresh_all_caches()

        self._bg_thread = threading.Thread(target=_sync_loop, daemon=True, name="DojoSDK-DatasetUpdater")
        self._bg_thread.start()
        logger.info(f"Started background sync thread (interval: {interval_days} days).")

    def stop_background_sync(self) -> None:
        if self._bg_thread and self._bg_thread.is_alive():
            self._stop_event.set()
            self._bg_thread.join(timeout=2.0)
            logger.info("Stopped background sync thread.")

    def preload(self, paths: list[str]) -> None:
        """Preload specific resources into cache ahead of time."""
        from dojo.datasource.registry import resolve
        from tqdm import tqdm
        from concurrent.futures import ThreadPoolExecutor, as_completed

        total = len(paths)
        if total == 0:
            return

        specs = [(i, path, resolve(path)) for i, path in enumerate(paths, start=1)]
        valid_specs = [(i, p, s) for i, p, s in specs if s]

        for i, path, spec in specs:
            if not spec:
                logger.warning(f"[{i}/{total}] Cannot preload {path}: endpoint not registered.")

        def _do_preload(i, path, spec):
            try:
                logger.debug(f"[{i}/{total}] 开始预加载 {path} ...")
                if spec.path_template.endswith(".parquet"):
                    self._load_dataset(spec, {}, refresh=True)
                logger.debug(f"[{i}/{total}] 成功预加载 {path}")
            except Exception as e:
                logger.error(f"[{i}/{total}] 预加载 {path} 失败: {e}")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(_do_preload, i, path, spec) for i, path, spec in valid_specs]
            for _ in tqdm(as_completed(futures), total=len(futures), desc="Preloading DojoSDK data"):
                pass

    def cleanup_cache(self) -> dict:
        """
        Scans the Hugging Face local cache directory and deletes all revisions
        except the latest one for each repository.
        Returns a dictionary summarizing the freed space.
        """
        try:
            from huggingface_hub import scan_cache_dir
        except ImportError:
            logger.error("Cache cleanup requires 'huggingface_hub'.")
            return {"error": "huggingface_hub is not installed"}

        # Scan the configured HF cache directory
        cache_info = scan_cache_dir(self._cfg.cache_dir)
        freed_summary = {}
        total_freed_bytes = 0

        for repo in cache_info.repos:
            if len(repo.revisions) <= 1:
                continue

            # Sort revisions by last_modified descending (newest first)
            sorted_revisions = sorted(repo.revisions, key=lambda r: r.last_modified, reverse=True)

            # Keep the newest, delete the rest
            older_revisions = [rev.commit_hash for rev in sorted_revisions[1:]]

            if older_revisions:
                strategy = cache_info.delete_revisions(*older_revisions)
                expected_freed = strategy.expected_freed_size
                strategy.execute()
                freed_summary[repo.repo_id] = strategy.expected_freed_size_str
                total_freed_bytes += expected_freed
                logger.info(f"Cleaned up {len(older_revisions)} older revisions for {repo.repo_id}, freed {strategy.expected_freed_size_str}")

        def format_bytes(size):
            for unit in ["B", "KB", "MB", "GB", "TB"]:
                if size < 1024.0:
                    return f"{size:.1f}{unit}"
                size /= 1024.0
            return f"{size:.1f}PB"

        result = {"freed_space": format_bytes(total_freed_bytes), "details": freed_summary, "message": "Cache cleanup complete."}
        logger.info(f"Cache cleanup complete. Total freed: {result['freed_space']}")
        return result


class HuggingFaceKlineDataSource(HuggingFaceDataSource):
    """
    A specialized HuggingFaceDataSource that pre-groups kline data by symbol
    for O(1) fetch performance during offline simulation.
    """

    def __init__(self, config: HFConfig | None = None) -> None:
        super().__init__(config)
        self._grouped_cache: dict[str, dict[str, list[dict]]] = {}

    def fetch(self, *, method: str, path: str, params: dict[str, Any], json: Any | None = None) -> Any:
        spec = resolve(path)
        if not spec:
            raise OfflineDataNotAvailableError(f"Endpoint {path} is not registered in the HuggingFace offline registry.")

        return super().fetch(method=method, path=path, params=params, json=json)

    def preload(self, paths: list[str]) -> None:
        super().preload(paths)
        self.fetch_df(path="/api/qdata/v1/stock/kline", params={}, refresh=True)

    def _fast_fetch_kline(self, path: str, spec: Any, params: dict[str, Any], json_body: Any | None) -> Any:
        merged = dict(params)
        if isinstance(json_body, dict):
            merged.update(json_body)

        # 1. Ensure the underlying dataset is loaded and cached
        table = self._load_dataset(spec, merged)
        cache_key = f"{spec.repo_id}/{self._render_template(spec.path_template, merged)}"

        # 2. Pre-group data if not already done
        if cache_key not in self._grouped_cache:
            self._grouped_cache[cache_key] = self._build_grouped_data(table, spec)

        grouped_data = self._grouped_cache[cache_key]

        # 3. Resolve requested symbols
        symbols = merged.get(spec.symbol_param, "")
        if isinstance(symbols, str):
            symbols = symbols.split(",") if "," in symbols else [symbols]
        elif not isinstance(symbols, (list, tuple, set)):
            symbols = [symbols]

        # 4. O(1) Fast fetch
        limit = merged.get(spec.limit_param)
        results = []
        for sym in symbols:
            if not sym:
                continue
            sym_rows = grouped_data.get(sym, [])
            if isinstance(limit, int) and limit > 0:
                sym_rows = sym_rows[:limit]
            results.extend(sym_rows)

        data: Any = {"total_num": len(results), "data": results} if spec.envelope == "list" else (results[0] if results else {})
        return {"code": 0, "message": "ok", "data": data}

    def _build_grouped_data(self, table, spec) -> dict[str, list[dict]]:
        import datetime
        import json
        from collections import defaultdict

        rows = table.to_pylist()

        json_cols = spec.json_columns or []
        if not json_cols and table.schema.metadata and b"dojosdk:json_columns" in table.schema.metadata:
            json_cols = table.schema.metadata[b"dojosdk:json_columns"].decode("utf-8").split(",")

        json_cols_set = set(json_cols)

        for row in rows:
            for col in json_cols_set:
                val = row.get(col)
                if isinstance(val, str):
                    try:
                        row[col] = json.loads(val)
                    except json.JSONDecodeError:
                        pass

            for k, v in row.items():
                if isinstance(v, (datetime.datetime, datetime.date)):
                    row[k] = v.isoformat()

        grouped = defaultdict(list)
        sym_field = spec.symbol_field
        for row in rows:
            sym = row.get(sym_field)
            if sym is not None:
                grouped[sym].append(row)

        if spec.time_field:
            for sym, sym_rows in grouped.items():
                sym_rows.sort(key=lambda x: x.get(spec.time_field, ""), reverse=spec.order_desc)

        return dict(grouped)
