from __future__ import annotations

import os
from typing import Mapping, Union, TYPE_CHECKING
from functools import cached_property
import httpx

if TYPE_CHECKING:
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

from dojo.client.base import SyncAPIClient
from dojo._exceptions import DojoError


class Dojo(SyncAPIClient):
    """Synchronous Dojo API Client."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout: Union[float, httpx.Timeout] = 300.0,
        max_retries: int = 1,
        http_client: httpx.Client | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        return_raw_data: bool = True,
    ) -> None:
        """Constructs a new synchronous Dojo client instance.

        Parameters
        ----------
        api_key : str, optional
            The token used to authenticate requests. If not provided, it is loaded
            from the DOJO_API_KEY environment variable.
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
        """
        from dojo.datasource.config import is_online, HFConfig
        from dojo.datasource.huggingface import HuggingFaceKlineDataSource

        self._online = is_online()

        api_key = api_key or os.environ.get("DOJO_API_KEY")
        if self._online and not api_key:
            raise DojoError("Missing authentication credentials. Please pass an `api_key` or set " "the `DOJO_API_KEY` environment variable.")
        self.api_key = api_key

        self._data_source = None
        if not self._online:
            self._data_source = HuggingFaceKlineDataSource(HFConfig.from_env())

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
        return {"Authorization": f"Bearer {self.api_key}"}

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

    def preload_offline_data(self, paths: list[str] | None = None) -> None:
        """Preload specific offline data resources into memory to avoid latency on first request."""
        if self._data_source is not None and hasattr(self._data_source, "preload"):
            if paths is None:
                from dojo.datasource.registry import HF_REGISTRY

                paths = list(HF_REGISTRY.keys())
            self._data_source.preload(paths)

    def upload_dataset(self, dataset_name: str, local_folder: str, token: str | None = None) -> None:
        """Uploads a local folder as a dataset to HuggingFace Hub."""
        from dojo.datasource.upload import upload_dataset as sync_upload_dataset

        sync_upload_dataset(dataset_name, local_folder, token)

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
