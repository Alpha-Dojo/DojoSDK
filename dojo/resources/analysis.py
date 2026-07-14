from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import AnalysisMarketDynamicsResponse, AnalysisTopicDiscoveriesResponse


class Analysis(SyncAPIResource):

    def get_market_dynamics(
        self,
        *,
        market: str | None = None,
        category: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> AnalysisMarketDynamicsResponse:
        """Retrieves market dynamics analysis data.

        Parameters
        ----------
        market : str, optional
            Market filtering.
        category : str, optional
            Category filtering.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if category is not None:
            params["category"] = category
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=AnalysisMarketDynamicsResponse,
            options={"params": params},
        )

    market_dynamics = get_market_dynamics

    def get_topic_discoveries(
        self,
        *,
        market: str | None = None,
        topic_id: str | None = None,
        topic_type: str | None = None,
        limit: int | None = None,
    ) -> AnalysisTopicDiscoveriesResponse:
        """Retrieves topic discoveries data.

        Parameters
        ----------
        market : str, optional
            Market filtering.
        topic_id : str, optional
            Topic ID filtering.
        topic_type : str, optional
            Topic type filtering.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if topic_id is not None:
            params["topic_id"] = topic_id
        if topic_type is not None:
            params["topic_type"] = topic_type
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/analysis/topic_discoveries",
            cast_to=AnalysisTopicDiscoveriesResponse,
            options={"params": params},
        )

    topic_discoveries = get_topic_discoveries


class AsyncAnalysis(AsyncAPIResource):

    async def get_market_dynamics(
        self,
        *,
        market: str | None = None,
        category: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> AnalysisMarketDynamicsResponse:
        """Retrieves market dynamics analysis data asynchronously.

        Parameters
        ----------
        market : str, optional
            Market filtering.
        category : str, optional
            Category filtering.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if category is not None:
            params["category"] = category
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=AnalysisMarketDynamicsResponse,
            options={"params": params},
        )

    market_dynamics = get_market_dynamics

    async def get_topic_discoveries(
        self,
        *,
        market: str | None = None,
        topic_id: str | None = None,
        topic_type: str | None = None,
        limit: int | None = None,
    ) -> AnalysisTopicDiscoveriesResponse:
        """Retrieves topic discoveries data asynchronously.

        Parameters
        ----------
        market : str, optional
            Market filtering.
        topic_id : str, optional
            Topic ID filtering.
        topic_type : str, optional
            Topic type filtering.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if topic_id is not None:
            params["topic_id"] = topic_id
        if topic_type is not None:
            params["topic_type"] = topic_type
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/analysis/topic_discoveries",
            cast_to=AnalysisTopicDiscoveriesResponse,
            options={"params": params},
        )

    topic_discoveries = get_topic_discoveries
