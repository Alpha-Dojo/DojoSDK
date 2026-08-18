from __future__ import annotations

from typing import Any
from dojo._compat import model_dump, model_validate
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    AnalysisMarketDynamicsResponse,
    AnalysisTopicDiscoveriesResponse,
    AttributionFactorWriteRequest,
    AttributionFactorWriteResponse,
    MarketDynamicsCreateResponse,
    AttributionFactorResponse,
    SectorBriefExtractListResponse,
    SectorBriefExtractWriteRequest,
    SectorBriefExtractWriteResponse,
)


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

    def get_attribution_factor(
        self,
        *,
        market: str | None = None,
        sector_id: int | str | None = None,
        scope: str | list[str] | None = None,
        factor_topic: str | None = None,
        role: str | None = None,
        payload_status: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> AttributionFactorResponse:
        """Retrieves attribution factor analysis data.

        Parameters
        ----------
        market : str, optional
            Market filtering (e.g. 'cn', 'hk', 'us').
        sector_id : str, optional
            Sector ID filtering.
        scope : str or list of str, optional
            Scope filtering (e.g. 'l1', 'l2', 'l3').
        factor_topic : str, optional
            Factor topic filtering.
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
        if sector_id is not None:
            params["sector_id"] = sector_id
        if scope is not None:
            params["scope"] = scope
        if factor_topic is not None:
            params["factor_topic"] = factor_topic
        if role is not None:
            params["role"] = role
        if payload_status is not None:
            params["payload_status"] = payload_status
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/analysis/attribution_factor",
            cast_to=AttributionFactorResponse,
            options={"params": params},
        )

    attribution_factor = get_attribution_factor

    def create_attribution_factor(
        self,
        *,
        body: AttributionFactorWriteRequest | dict[str, Any],
    ) -> AttributionFactorWriteResponse:
        """Atomically create or update attribution factors."""
        request = body if isinstance(body, AttributionFactorWriteRequest) else model_validate(AttributionFactorWriteRequest, body)
        return self._post(
            "/api/qdata/v1/analysis/attribution_factor",
            cast_to=AttributionFactorWriteResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    def list_sector_brief_extract(
        self,
        *,
        market: str | None = None,
        sector_id: int | str | None = None,
        as_of_date: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> SectorBriefExtractListResponse:
        """List extracted sector briefs."""
        params = {
            key: value
            for key, value in {
                "market": market,
                "sector_id": sector_id,
                "as_of_date": as_of_date,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
            }.items()
            if value is not None
        }
        return self._get(
            "/api/qdata/v1/analysis/sector_brief_extract",
            cast_to=SectorBriefExtractListResponse,
            options={"params": params},
        )

    get_sector_brief_extract = list_sector_brief_extract
    sector_brief_extract = list_sector_brief_extract

    def create_sector_brief_extract(
        self,
        *,
        body: SectorBriefExtractWriteRequest | dict[str, Any],
    ) -> SectorBriefExtractWriteResponse:
        """Atomically create or update extracted sector briefs."""
        request = body if isinstance(body, SectorBriefExtractWriteRequest) else model_validate(SectorBriefExtractWriteRequest, body)
        return self._post(
            "/api/qdata/v1/analysis/sector_brief_extract",
            cast_to=SectorBriefExtractWriteResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    def create_market_dynamics(
        self,
        *,
        market: str,
        trading_date: str,
        event_time: str,
        event_summary: dict[str, Any],
        sector_impacts: list[dict[str, Any]],
        generation_time: str | None = None,
        event_rank: str | None = None,
        confidence: str | None = None,
        driver_status: str | None = None,
        index_evidence: str | None = None,
    ) -> MarketDynamicsCreateResponse:
        """Create a single market dynamics record."""
        payload = {
            "market": market,
            "trading_date": trading_date,
            "event_time": event_time,
            "event_rank": event_rank,
            "confidence": confidence,
            "driver_status": driver_status,
            "index_evidence": index_evidence,
            "event_summary": event_summary,
            "sector_impacts": sector_impacts,
        }
        if generation_time is not None:
            payload["generation_time"] = generation_time
        return self._post(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=MarketDynamicsCreateResponse,
            options={"json": payload},
        )

    def update_market_dynamics(
        self,
        *,
        event_time: str,
        event_summary: dict[str, Any],
        sector_impacts: list[dict[str, Any]],
    ) -> MarketDynamicsCreateResponse:
        """Update a single market dynamics record."""
        return self._put(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=MarketDynamicsCreateResponse,
            options={
                "json": {
                    "event_time": event_time,
                    "event_summary": event_summary,
                    "sector_impacts": sector_impacts,
                }
            },
        )

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

    async def get_attribution_factor(
        self,
        *,
        market: str | None = None,
        sector_id: str | None = None,
        scope: str | list[str] | None = None,
        factor_topic: str | None = None,
        role: str | None = None,
        payload_status: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> AttributionFactorResponse:
        """Retrieves attribution factor analysis data asynchronously.

        Parameters
        ----------
        market : str, optional
            Market filtering (e.g. 'cn', 'hk', 'us').
        sector_id : str, optional
            Sector ID filtering.
        scope : str or list of str, optional
            Scope filtering (e.g. 'l1', 'l2', 'l3').
        factor_topic : str, optional
            Factor topic filtering.
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
        if sector_id is not None:
            params["sector_id"] = sector_id
        if scope is not None:
            params["scope"] = scope
        if factor_topic is not None:
            params["factor_topic"] = factor_topic
        if role is not None:
            params["role"] = role
        if payload_status is not None:
            params["payload_status"] = payload_status
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/analysis/attribution_factor",
            cast_to=AttributionFactorResponse,
            options={"params": params},
        )

    attribution_factor = get_attribution_factor

    async def create_attribution_factor(
        self,
        *,
        body: AttributionFactorWriteRequest | dict[str, Any],
    ) -> AttributionFactorWriteResponse:
        """Atomically create or update attribution factors asynchronously."""
        request = body if isinstance(body, AttributionFactorWriteRequest) else model_validate(AttributionFactorWriteRequest, body)
        return await self._post(
            "/api/qdata/v1/analysis/attribution_factor",
            cast_to=AttributionFactorWriteResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    async def list_sector_brief_extract(
        self,
        *,
        market: str | None = None,
        sector_id: str | None = None,
        as_of_date: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> SectorBriefExtractListResponse:
        """List extracted sector briefs asynchronously."""
        params = {
            key: value
            for key, value in {
                "market": market,
                "sector_id": sector_id,
                "as_of_date": as_of_date,
                "start_date": start_date,
                "end_date": end_date,
                "limit": limit,
            }.items()
            if value is not None
        }
        return await self._get(
            "/api/qdata/v1/analysis/sector_brief_extract",
            cast_to=SectorBriefExtractListResponse,
            options={"params": params},
        )

    get_sector_brief_extract = list_sector_brief_extract
    sector_brief_extract = list_sector_brief_extract

    async def create_sector_brief_extract(
        self,
        *,
        body: SectorBriefExtractWriteRequest | dict[str, Any],
    ) -> SectorBriefExtractWriteResponse:
        """Atomically create or update extracted sector briefs asynchronously."""
        request = body if isinstance(body, SectorBriefExtractWriteRequest) else model_validate(SectorBriefExtractWriteRequest, body)
        return await self._post(
            "/api/qdata/v1/analysis/sector_brief_extract",
            cast_to=SectorBriefExtractWriteResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    async def create_market_dynamics(
        self,
        *,
        market: str,
        trading_date: str,
        event_time: str,
        event_summary: dict[str, Any],
        sector_impacts: list[dict[str, Any]],
        generation_time: str | None = None,
        event_rank: str | None = None,
        confidence: str | None = None,
        driver_status: str | None = None,
        index_evidence: str | None = None,
    ) -> MarketDynamicsCreateResponse:
        """Create a single market dynamics record asynchronously."""
        payload = {
            "market": market,
            "trading_date": trading_date,
            "event_time": event_time,
            "event_rank": event_rank,
            "confidence": confidence,
            "driver_status": driver_status,
            "index_evidence": index_evidence,
            "event_summary": event_summary,
            "sector_impacts": sector_impacts,
        }
        if generation_time is not None:
            payload["generation_time"] = generation_time
        return await self._post(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=MarketDynamicsCreateResponse,
            options={"json": payload},
        )

    async def update_market_dynamics(
        self,
        *,
        event_time: str,
        event_summary: dict[str, Any],
        sector_impacts: list[dict[str, Any]],
    ) -> MarketDynamicsCreateResponse:
        """Update a single market dynamics record asynchronously."""
        return await self._put(
            "/api/qdata/v1/analysis/market_dynamics",
            cast_to=MarketDynamicsCreateResponse,
            options={
                "json": {
                    "event_time": event_time,
                    "event_summary": event_summary,
                    "sector_impacts": sector_impacts,
                }
            },
        )

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
