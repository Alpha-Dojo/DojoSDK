from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    StrategyDemoResponse,
    StrategyPerformanceResponse,
)


class Strategy(SyncAPIResource):

    def get_demo(self) -> StrategyDemoResponse:
        """Retrieves classic demo strategies.

        Returns
        -------
        StrategyDemoResponse
            The list of demo strategies and metadata.
        """
        return self._get("/api/qdata/v1/strategy/demo", cast_to=StrategyDemoResponse)

    def get_performance(
        self,
        *,
        strategy_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
        bench_mark: str | None = None,
    ) -> StrategyPerformanceResponse:
        """Retrieves classic strategy performance indices.

        Parameters
        ----------
        strategy_id : str
            The identifier of the strategy (e.g. strategy key).
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-01-01T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of performance data points to return.
        bench_mark : str, optional
            Benchmark symbol to compare performance against (e.g. SPY).
        """
        params: dict[str, Any] = {"strategy_id": strategy_id}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        if bench_mark is not None:
            params["bench_mark"] = bench_mark
        return self._get("/api/qdata/v1/strategy/performance", cast_to=StrategyPerformanceResponse, options={"params": params})


class AsyncStrategy(AsyncAPIResource):

    async def get_demo(self) -> StrategyDemoResponse:
        """Retrieves classic demo strategies asynchronously.

        Returns
        -------
        StrategyDemoResponse
            The list of demo strategies and metadata.
        """
        return await self._get("/api/qdata/v1/strategy/demo", cast_to=StrategyDemoResponse)

    async def get_performance(
        self,
        *,
        strategy_id: str,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
        bench_mark: str | None = None,
    ) -> StrategyPerformanceResponse:
        """Retrieves classic strategy performance indices asynchronously.

        Parameters
        ----------
        strategy_id : str
            The identifier of the strategy (e.g. strategy key).
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-01-01T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of performance data points to return.
        bench_mark : str, optional
            Benchmark symbol to compare performance against (e.g. SPY).
        """
        params: dict[str, Any] = {"strategy_id": strategy_id}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        if bench_mark is not None:
            params["bench_mark"] = bench_mark
        return await self._get("/api/qdata/v1/strategy/performance", cast_to=StrategyPerformanceResponse, options={"params": params})
