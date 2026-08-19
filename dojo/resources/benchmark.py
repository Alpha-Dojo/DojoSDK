from __future__ import annotations

from typing import Any, List
from dojo.resources.base import AsyncAPIResource, SyncAPIResource, normalize_naive_iso_datetime
from dojo.types.models import (
    BenchmarkCatalogResponse,
    BenchmarkKLineResponse,
    BenchmarkPriceResponse,
    BenchmarkPerformanceResponse,
    SectorPrecomputedMarketBenchmarkDailyResponse,
)


def _params(**values: Any) -> dict[str, Any]:
    return {name: value for name, value in values.items() if value is not None}


class Benchmark(SyncAPIResource):

    def get_info(
        self,
        *,
        tickers: str | None = None,
        category: str | None = None,
        sub_category: str | None = None,
        ticker_type: str | None = None,
    ) -> BenchmarkCatalogResponse:
        return self._get(
            "/api/qdata/v1/benchmark",
            cast_to=BenchmarkCatalogResponse,
            options={
                "params": _params(
                    tickers=tickers,
                    category=category,
                    sub_category=sub_category,
                    ticker_type=ticker_type,
                )
            },
        )

    def get_market_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedMarketBenchmarkDailyResponse:
        params = _params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return self._get(
            "/api/qdata/v1/market/benchmarks/daily",
            cast_to=SectorPrecomputedMarketBenchmarkDailyResponse,
            options={"params": params},
        )

    def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        price_adj_type: str | None = None,
        price_adj_date: str | None = None,
        limit: int | None = None,
    ) -> BenchmarkKLineResponse:
        """Retrieves historical kline (candlestick) data for standard indices benchmarks.

        Parameters
        ----------
        symbol : str
            The benchmark symbol (e.g. S&P500 index key).
        kline_t : str, optional
            Kline interval size (e.g. 1m, 1h, 1d).
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-05-28T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        price_adj_type : str, optional
            Price adjustment type.
        price_adj_date : str, optional
            Reference date for adjustment.
        limit : int, optional
            Max number of kline data points to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = normalize_naive_iso_datetime(start_time)
        if end_time is not None:
            params["end_time"] = normalize_naive_iso_datetime(end_time)
        if price_adj_type is not None:
            params["price_adj_type"] = price_adj_type
        if price_adj_date is not None:
            params["price_adj_date"] = normalize_naive_iso_datetime(price_adj_date)
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/benchmark/kline",
            cast_to=BenchmarkKLineResponse,
            options={"params": params},
        )

    kline = get_kline

    def get_price(self, *, symbols: List[str] | None = None) -> BenchmarkPriceResponse:
        """Retrieves last/current price for standard indices benchmarks.

        Parameters
        ----------
        symbols : list of str, optional
            Target benchmark index symbols list.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return self._get(
            "/api/qdata/v1/benchmark/cur_price",
            cast_to=BenchmarkPriceResponse,
            options={"params": params},
        )

    def get_performance(
        self,
        *,
        symbol: str,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> BenchmarkPerformanceResponse:
        """Retrieves comparative performance values for a benchmark index.

        Parameters
        ----------
        symbol : str
            The benchmark symbol (e.g. BTC).
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if start_time is not None:
            params["start_time"] = normalize_naive_iso_datetime(start_time)
        if end_time is not None:
            params["end_time"] = normalize_naive_iso_datetime(end_time)
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/benchmark/performance",
            cast_to=BenchmarkPerformanceResponse,
            options={"params": params},
        )

    def get_catalog(self) -> BenchmarkCatalogResponse:
        """Retrieves benchmark catalog metadata used for default selection and labels."""
        return self._get("/api/qdata/v1/benchmark/catalog", cast_to=BenchmarkCatalogResponse)


class AsyncBenchmark(AsyncAPIResource):

    async def get_info(
        self,
        *,
        tickers: str | None = None,
        category: str | None = None,
        sub_category: str | None = None,
        ticker_type: str | None = None,
    ) -> BenchmarkCatalogResponse:
        return await self._get(
            "/api/qdata/v1/benchmark",
            cast_to=BenchmarkCatalogResponse,
            options={
                "params": _params(
                    tickers=tickers,
                    category=category,
                    sub_category=sub_category,
                    ticker_type=ticker_type,
                )
            },
        )

    async def get_market_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedMarketBenchmarkDailyResponse:
        params = _params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return await self._get(
            "/api/qdata/v1/market/benchmarks/daily",
            cast_to=SectorPrecomputedMarketBenchmarkDailyResponse,
            options={"params": params},
        )

    async def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        price_adj_type: str | None = None,
        price_adj_date: str | None = None,
        limit: int | None = None,
    ) -> BenchmarkKLineResponse:
        """Retrieves historical kline (candlestick) data for standard indices benchmarks asynchronously.

        Parameters
        ----------
        symbol : str
            The benchmark symbol (e.g. S&P500 index key).
        kline_t : str, optional
            Kline interval size (e.g. 1m, 1h, 1d).
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-05-28T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        price_adj_type : str, optional
            Price adjustment type.
        price_adj_date : str, optional
            Reference date for adjustment.
        limit : int, optional
            Max number of kline data points to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = normalize_naive_iso_datetime(start_time)
        if end_time is not None:
            params["end_time"] = normalize_naive_iso_datetime(end_time)
        if price_adj_type is not None:
            params["price_adj_type"] = price_adj_type
        if price_adj_date is not None:
            params["price_adj_date"] = normalize_naive_iso_datetime(price_adj_date)
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/benchmark/kline",
            cast_to=BenchmarkKLineResponse,
            options={"params": params},
        )

    kline = get_kline

    async def get_price(self, *, symbols: List[str] | None = None) -> BenchmarkPriceResponse:
        """Retrieves last/current price for standard indices benchmarks asynchronously.

        Parameters
        ----------
        symbols : list of str, optional
            Target benchmark index symbols list.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return await self._get(
            "/api/qdata/v1/benchmark/cur_price",
            cast_to=BenchmarkPriceResponse,
            options={"params": params},
        )

    async def get_performance(
        self,
        *,
        symbol: str,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> BenchmarkPerformanceResponse:
        """Retrieves comparative performance values for a benchmark index asynchronously.

        Parameters
        ----------
        symbol : str
            The benchmark symbol (e.g. BTC).
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if start_time is not None:
            params["start_time"] = normalize_naive_iso_datetime(start_time)
        if end_time is not None:
            params["end_time"] = normalize_naive_iso_datetime(end_time)
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/benchmark/performance",
            cast_to=BenchmarkPerformanceResponse,
            options={"params": params},
        )

    async def get_catalog(self) -> BenchmarkCatalogResponse:
        """Retrieves benchmark catalog metadata used for default selection and labels asynchronously."""
        return await self._get("/api/qdata/v1/benchmark/catalog", cast_to=BenchmarkCatalogResponse)
