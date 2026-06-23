from __future__ import annotations

from typing import Any

from dojo.datasource.config import HFConfig
from dojo.datasource.registry import HFEndpointSpec, resolve
from dojo._exceptions import OfflineDataNotAvailableError
from dojo.logging import logger


class HuggingFaceDataSource:
    def __init__(self, config: HFConfig | None = None) -> None:
        import threading

        self._cfg = config or HFConfig.from_env()
        self._table_cache: dict[str, Any] = {}
        self._bg_thread: threading.Thread | None = None
        self._stop_event = threading.Event()

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

    def _load_dataset(self, spec: HFEndpointSpec, params: dict[str, Any]):
        try:
            from datasets import load_dataset
        except ImportError:
            raise OfflineDataNotAvailableError("Offline huggingface data source requires 'datasets' and 'pyarrow'. " "Install with `pip install dojosdk[huggingface]`.")

        import os

        relative = self._render_template(spec.path_template, params)
        cache_key = f"{spec.repo_id}/{relative}"

        if cache_key in self._table_cache:
            return self._table_cache[cache_key]

        # Enforce strict offline mode if local_only is set
        if self._cfg.local_only:
            os.environ["HF_DATASETS_OFFLINE"] = "1"

        try:
            ds = load_dataset(
                spec.repo_id,
                data_files=relative,
                revision=self._cfg.revision,
                token=self._cfg.token,
                cache_dir=os.path.join(self._cfg.cache_dir, "datasets"),
                split="train",
            )
            table = ds.data.table
            self._table_cache[cache_key] = table
            return table
        except Exception as err:
            if spec.fallback_template:
                fb = self._render_template(spec.fallback_template, params)
                cache_key_fb = f"{spec.repo_id}/{fb}"

                if cache_key_fb in self._table_cache:
                    return self._table_cache[cache_key_fb]

                logger.warning(f"Failed to fetch main file {relative}, falling back to {fb}: {err}")
                try:
                    ds = load_dataset(
                        spec.repo_id,
                        data_files=fb,
                        revision=self._cfg.revision,
                        token=self._cfg.token,
                        cache_dir=os.path.join(self._cfg.cache_dir, "datasets"),
                        split="train",
                    )
                    table = ds.data.table
                    self._table_cache[cache_key_fb] = table
                    return table
                except Exception as fb_err:
                    raise OfflineDataNotAvailableError(f"Cannot fetch offline file {spec.repo_id}/{fb}: {fb_err}") from fb_err
            raise OfflineDataNotAvailableError(f"Cannot fetch offline file {spec.repo_id}/{relative}: {err}") from err

    @staticmethod
    def _render_template(template: str, params: dict[str, Any]) -> str:
        try:
            return template.format(**params)
        except KeyError as e:
            raise OfflineDataNotAvailableError(f"Offline file path template {template!r} is missing required parameter {e}") from e

    def _apply_filters(self, table, spec: HFEndpointSpec, params: dict[str, Any]) -> list[dict]:
        try:
            import pyarrow.compute as pc
        except ImportError:
            raise OfflineDataNotAvailableError("Offline data processing requires 'pyarrow'.")

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
        try:
            from datasets import load_dataset
        except ImportError:
            return

        import os
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
                ds = load_dataset(
                    spec.repo_id,
                    data_files=relative,
                    revision=self._cfg.revision,
                    token=self._cfg.token,
                    cache_dir=os.path.join(self._cfg.cache_dir, "datasets"),
                    split="train",
                    download_mode="force_redownload",
                )
                self._table_cache[cache_key] = ds.data.table
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

        for path in paths:
            spec = resolve(path)
            if not spec:
                logger.warning(f"Cannot preload {path}: endpoint not registered.")
                continue
            try:
                self._load_dataset(spec, {})
                logger.info(f"Preloaded dataset for {path}")
            except Exception as e:
                logger.warning(f"Failed to preload {path}: {e}")


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

        if spec.symbol_field and spec.symbol_param in params and path.endswith("/kline"):
            return self._fast_fetch_kline(path, spec, params, json)

        return super().fetch(method=method, path=path, params=params, json=json)

    def preload(self, paths: list[str]) -> None:
        super().preload(paths)
        from dojo.datasource.registry import resolve

        for path in paths:
            if not path.endswith("/kline"):
                continue
            spec = resolve(path)
            if not spec:
                continue

            try:
                table = self._load_dataset(spec, {})
                cache_key = f"{spec.repo_id}/{self._render_template(spec.path_template, {})}"
                if cache_key not in self._grouped_cache:
                    logger.info(f"Pre-grouping kline data for {cache_key}...")
                    self._grouped_cache[cache_key] = self._build_grouped_data(table, spec)
                    logger.info(f"Pre-grouping complete for {cache_key}.")
            except Exception as e:
                logger.warning(f"Failed to pre-group {path}: {e}")

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
