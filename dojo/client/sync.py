from __future__ import annotations

import os
import warnings
from typing import Mapping, Union, TYPE_CHECKING
from functools import cached_property
import httpx

if TYPE_CHECKING:
    from dojo.datasource.config import HFConfig
    from dojo.resources.stocks import Stocks
    from dojo.resources.market_data import MarketData, Indices, Instruments
    from dojo.resources.macro import Macro
    from dojo.resources.benchmark import Benchmark
    from dojo.resources.concepts import Concepts
    from dojo.resources.news import News
    from dojo.resources.forex import Forex
    from dojo.resources.user import User
    from dojo.resources.sectors import Sectors
    from dojo.resources.strategy import Strategy
    from dojo.resources.cache import Cache
    from dojo.resources.analysis import Analysis
    from dojo.resources.etf import Etf
    from dojo.resources.factor import Factor

from dojo.client.base import SyncAPIClient
from dojo._exceptions import DojoError, OfflineDataNotAvailableError
from dojo.types.snapshot import SnapshotGCResult, SnapshotRef, SnapshotSyncResult


class Dojo(SyncAPIClient):
    """Synchronous Dojo API Client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        anonymous: bool = False,
        base_url: str | None = None,
        timeout: Union[float, httpx.Timeout] = 300.0,
        max_retries: int = 1,
        http_client: httpx.Client | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        return_raw_data: bool = True,
        online: bool | None = None,
        offline_config: HFConfig | None = None,
    ) -> None:
        """Constructs a new synchronous Dojo client instance.

        Parameters
        ----------
        api_key : str, optional
            The token used to authenticate requests. If not provided, it is loaded
            from the DOJO_API_KEY environment variable.
        anonymous : bool, default False
            Read only the public research list without credentials. Ignores API keys
            and strips Authorization/Cookie; protected operations are rejected locally.
        base_url : str, optional
            The base URL of the Dojo API. Defaults to https://api.flowhale.ai.
        timeout : float or httpx.Timeout, default 300.0
            Maximum time (in seconds) to wait for an HTTP request before timing out.
        max_retries : int, default 1
            Number of times to retry failed requests on connection errors/rate limits.
        http_client : httpx.Client, optional
            A custom httpx Client instance to use for sending requests.
        default_headers : dict, optional
            A dictionary of custom HTTP headers to send with every request.
        default_query : dict, optional
            A dictionary of custom query parameters to send with every request.
        return_raw_data : bool, default True
            If True, API responses are returned as native Python dictionaries/lists,
            skipping Pydantic model validation.
        online : bool, optional
            Explicitly select online mode. When omitted, DOJO_ONLINE is used.
        offline_config : HFConfig, optional
            Explicit offline datasource settings used when online is False.
        """
        from dojo.datasource.config import is_online, HFConfig
        from dojo.datasource.huggingface import HuggingFaceKlineDataSource

        self._online = is_online() if online is None else bool(online)

        self._anonymous = anonymous
        if anonymous and not self._online:
            raise DojoError("Anonymous mode requires online access")
        api_key = None if anonymous else (api_key or os.environ.get("DOJO_API_KEY"))
        if self._online and not api_key and not anonymous:
            raise DojoError("Missing authentication credentials. Please pass an `api_key` or set " "the `DOJO_API_KEY` environment variable.")
        self.api_key = api_key

        self._data_source = None
        if not self._online:
            hf_config = offline_config or HFConfig.from_env()
            if "DOJO_HF_DOWNLOAD_TIMEOUT" not in os.environ:
                timeout_seconds = float(timeout) if isinstance(timeout, (int, float)) else timeout.read
                if timeout_seconds is not None and timeout_seconds > 0:
                    hf_config.download_timeout_seconds = timeout_seconds
            if "DOJO_HF_MAX_RETRIES" not in os.environ:
                hf_config.max_download_retries = max(0, max_retries)
            self._data_source = HuggingFaceKlineDataSource(hf_config)

        base_url = base_url or os.environ.get("DOJO_BASE_URL") or "https://api.flowhale.ai"

        if http_client is None:
            # Default pool limits
            limits = httpx.Limits(max_connections=100, max_keepalive_connections=20)
            http_client = httpx.Client(
                limits=limits,
                timeout=timeout,
                follow_redirects=True,
            )
        self._client = http_client

        super().__init__(
            base_url=base_url,
            max_retries=max_retries,
            custom_headers=default_headers,
            custom_query=default_query,
            return_raw_data=return_raw_data,
        )

    @property
    def auth_headers(self) -> dict[str, str]:
        """Returns the authorization headers containing the Bearer token."""
        return {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}

    @property
    def default_headers(self) -> dict[str, str]:
        """Returns the default headers containing auth and telemetry details."""
        headers = super().default_headers
        headers.update(self.auth_headers)
        return headers

    def start_background_sync(self, interval_days: int = 1) -> None:
        """Starts a background daemon thread that refreshes offline datasets periodically.

        Parameters
        ----------
        interval_days : int
            The number of days between each refresh. Defaults to 1.
        """
        if self._data_source is not None and hasattr(self._data_source, "start_background_sync"):
            self._data_source.start_background_sync(interval_days=interval_days)

    def stop_background_sync(self) -> None:
        """Stops the background dataset refresh thread."""
        if self._data_source is not None and hasattr(self._data_source, "stop_background_sync"):
            self._data_source.stop_background_sync()

    def cancel_preload_offline_data(self) -> None:
        """Cancel an in-flight offline preload if the data source supports it."""
        cancel = getattr(self._data_source, "cancel_preload", None)
        if callable(cancel):
            cancel()

    def preload_offline_data(self, paths: list[str] | None = None) -> None:
        """Deprecated compatibility wrapper; use ensure_offline_snapshots()."""
        warnings.warn(
            "preload_offline_data() is deprecated and will be removed in the next " "DojoSDK major release; use ensure_offline_snapshots(paths=...).",
            DeprecationWarning,
            stacklevel=2,
        )
        if self._data_source is not None and hasattr(self._data_source, "preload"):
            if paths is None:
                from dojo.datasource.registry import HF_REGISTRY

                paths = list(HF_REGISTRY.keys())
            self._data_source.preload(paths)

    def ensure_offline_snapshots(
        self,
        *,
        paths: list[str] | None = None,
        repos: list[str] | None = None,
    ) -> list[SnapshotRef]:
        """Ensure explicitly selected offline snapshots exist locally."""
        if self._data_source is None:
            raise OfflineDataNotAvailableError("Snapshot synchronization is only available in offline mode.")
        return self._data_source.ensure_offline_snapshots(paths=paths, repos=repos)

    def sync_offline_snapshots(
        self,
        *,
        paths: list[str] | None = None,
        repos: list[str] | None = None,
        check_remote: bool = True,
        force: bool = False,
    ) -> SnapshotSyncResult:
        """Synchronize explicitly selected repositories with atomic publication."""
        if self._data_source is None:
            raise OfflineDataNotAvailableError("Snapshot synchronization is only available in offline mode.")
        return self._data_source.sync_offline_snapshots(
            paths=paths,
            repos=repos,
            check_remote=check_remote,
            force=force,
        )

    def gc_offline_snapshots(
        self,
        *,
        paths: list[str] | None = None,
        repos: list[str] | None = None,
        min_age_seconds: float = 7 * 24 * 60 * 60,
        keep_previous: int = 1,
        dry_run: bool = True,
    ) -> SnapshotGCResult:
        """Preview or run conservative cleanup of selected snapshot revisions."""
        if self._data_source is None:
            raise OfflineDataNotAvailableError("Snapshot cleanup is only available in offline mode.")
        return self._data_source.gc_offline_snapshots(
            paths=paths,
            repos=repos,
            min_age_seconds=min_age_seconds,
            keep_previous=keep_previous,
            dry_run=dry_run,
        )

    def upload_dataset(self, dataset_name: str, local_folder: str, token: str | None = None) -> None:
        """Uploads a local folder as a dataset to HuggingFace Hub."""
        from dojo.datasource.upload import upload_dataset as sync_upload_dataset

        sync_upload_dataset(dataset_name, local_folder, token)

    def download_dataset(self, dataset_name: str, local_folder: str, token: str | None = None) -> None:
        """Downloads a dataset from HuggingFace Hub to a local folder."""
        from dojo.datasource.upload import download_dataset as sync_download_dataset

        sync_download_dataset(dataset_name, local_folder, token)

    @cached_property
    def stocks(self) -> Stocks:
        """Access the stocks resource namespace for stock quotes, fundamentals, news, and metrics."""
        from dojo.resources.stocks import Stocks

        return Stocks(self)

    @cached_property
    def market_data(self) -> MarketData:
        """Access the market_data resource namespace for public real-time tickers, order books, and klines."""
        from dojo.resources.market_data import MarketData

        return MarketData(self)

    @cached_property
    def macro(self) -> Macro:
        """Access the macro resource namespace for macroeconomic data, news, and metrics."""
        from dojo.resources.macro import Macro

        return Macro(self)

    @cached_property
    def benchmark(self) -> Benchmark:
        """Access the benchmark resource namespace for index benchmarks and index klines."""
        from dojo.resources.benchmark import Benchmark

        return Benchmark(self)

    @cached_property
    def concepts(self) -> Concepts:
        """Access the concepts resource namespace for concept themes and constituents."""
        from dojo.resources.concepts import Concepts

        return Concepts(self)

    @cached_property
    def news(self) -> News:
        """Access the news resource namespace for general news, news sentiment scores, and events."""
        from dojo.resources.news import News

        return News(self)

    @cached_property
    def forex(self) -> Forex:
        """Access the forex resource namespace for forex quotes, klines, and symbol lists."""
        from dojo.resources.forex import Forex

        return Forex(self)

    @cached_property
    def user(self) -> User:
        """Access the user resource namespace for user traits management and analytics."""
        from dojo.resources.user import User

        return User(self)

    @cached_property
    def sectors(self) -> Sectors:
        """Access the sectors resource namespace for sector/industry listings and metrics."""
        from dojo.resources.sectors import Sectors

        return Sectors(self)

    @cached_property
    def strategy(self) -> Strategy:
        """Access the strategy resource namespace for classic strategy demos and backtest results."""
        from dojo.resources.strategy import Strategy

        return Strategy(self)

    @cached_property
    def cache(self) -> Cache:
        """Access the cache resource namespace for resetting/clearing cached data."""
        from dojo.resources.cache import Cache

        return Cache(self)

    @cached_property
    def indices(self) -> Indices:
        """Access the indices resource namespace for standard index list retrieval."""
        from dojo.resources.market_data import Indices

        return Indices(self)

    @cached_property
    def instruments(self) -> Instruments:
        """Access the instruments resource namespace for exchange tradable instruments listing."""
        from dojo.resources.market_data import Instruments

        return Instruments(self)

    @cached_property
    def analysis(self) -> Analysis:
        """Access the analysis resource namespace for market dynamics and other analyses."""
        from dojo.resources.analysis import Analysis

        return Analysis(self)

    @cached_property
    def etf(self) -> Etf:
        """Access etf holding portfolio"""
        from dojo.resources.etf import Etf

        return Etf(self)

    @cached_property
    def factor(self) -> Factor:
        """Access the factor resource namespace for querying factor tables and schemas."""
        from dojo.resources.factor import Factor

        return Factor(self)
