from __future__ import annotations

from typing import Any, Literal
from dojo._compat import model_dump, model_validate
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    AnalysisMarketDynamicsResponse,
    AnalysisTopicDiscoveriesResponse,
    AttributionFactorWriteRequest,
    AttributionFactorWriteResponse,
    MarketDynamicsCreateResponse,
    MarketMacroEventDailyRequest,
    MarketStructuredEventIngestResponse,
    MarketStructuredEventListResponse,
    AttributionFactorResponse,
    SectorBriefExtractListResponse,
    SectorBriefExtractWriteRequest,
    SectorBriefExtractWriteResponse,
    ResearchAggregateResponse,
    ResearchCreateRequest,
    ResearchUpdateRequest,
    ResearchDeleteResponse,
    ResearchListResponse,
    PublicResearchListResponse,
    ResearchResultListResponse,
    ResearchResultSnapshotRequest,
    ResearchResultWriteResponse,
    ResearchTimelineReplaceRequest,
    SectorL2EventCreateRequest,
    SectorL2EventCreateResponse,
    SectorL2EventListRequest,
    SectorL2EventListResponse,
    SectorL2EventResponse,
    SectorL2EventUpdateRequest,
)


class Analysis(SyncAPIResource):

    def list_sector_l2_events(
        self,
        *,
        id: int | None = None,
        as_of_date: str | None = None,
        market: str | None = None,
        kind_id: str | None = None,
        signal_type: str | None = None,
        source_scope: str | None = None,
        sector_id: int | None = None,
        ticker: str | None = None,
        event_datetime_from: str | None = None,
        event_datetime_to: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorL2EventListResponse:
        """List sector L2 events using the supported event filters."""
        request = model_validate(
            SectorL2EventListRequest,
            {
                "id": id,
                "as_of_date": as_of_date,
                "market": market,
                "kind_id": kind_id,
                "signal_type": signal_type,
                "source_scope": source_scope,
                "sector_id": sector_id,
                "ticker": ticker,
                "event_datetime_from": event_datetime_from,
                "event_datetime_to": event_datetime_to,
                "limit": limit,
                "offset": offset,
            },
        )
        return self._get(
            "/api/qdata/v1/analysis/research/sector_l2_events",
            cast_to=SectorL2EventListResponse,
            options={"params": model_dump(request, mode="json", exclude_none=True)},
        )

    def create_sector_l2_events(
        self,
        *,
        body: SectorL2EventCreateRequest | dict[str, Any],
    ) -> SectorL2EventCreateResponse:
        """Create one or more sector L2 events linked to one sector."""
        request = body if isinstance(body, SectorL2EventCreateRequest) else model_validate(SectorL2EventCreateRequest, body)
        return self._post(
            "/api/qdata/v1/analysis/research/sector_l2_events",
            cast_to=SectorL2EventCreateResponse,
            options={"json": model_dump(request, mode="json")},
        )

    def get_sector_l2_event(self, event_id: int) -> SectorL2EventResponse:
        """Get one sector L2 event by ID."""
        return self._get(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
        )

    def update_sector_l2_event(
        self,
        event_id: int,
        *,
        body: SectorL2EventUpdateRequest | dict[str, Any],
    ) -> SectorL2EventResponse:
        """Partially update one sector L2 event."""
        request = body if isinstance(body, SectorL2EventUpdateRequest) else model_validate(SectorL2EventUpdateRequest, body)
        return self._put(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
            options={"json": model_dump(request, mode="json", exclude_unset=True)},
        )

    def delete_sector_l2_event(self, event_id: int) -> SectorL2EventResponse:
        """Delete one sector L2 event and return its previous representation."""
        return self._delete(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
        )

    def list_market_research(
        self,
        *,
        scope: Literal["public", "mine", "starred"] | None = None,
        is_editor_pick: bool | None = None,
        sector_id: int | None = None,
        status: str | None = None,
        impact: Literal["medium", "high", "severe"] | None = None,
        timeline_source: Literal["producer", "manual"] | None = None,
        visibility: Literal["private", "public"] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResearchListResponse:
        """List public roots plus caller-owned roots; scope also supports the caller's starred view."""
        params = {
            key: value
            for key, value in {
                "scope": scope,
                "is_editor_pick": is_editor_pick,
                "sector_id": sector_id,
                "status": status,
                "impact": impact,
                "timeline_source": timeline_source,
                "visibility": visibility,
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return self._get(
            "/api/qdata/v1/analysis/research",
            cast_to=ResearchListResponse,
            options={"params": params},
        )

    def list_public_market_research(
        self,
        *,
        is_editor_pick: bool | None = None,
        sector_id: int | None = None,
        status: str | None = None,
        impact: Literal["medium", "high", "severe"] | None = None,
        timeline_source: Literal["producer", "manual"] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PublicResearchListResponse:
        """List strictly public research; caller-owned private roots are never included."""
        params = {
            key: value
            for key, value in {
                "is_editor_pick": is_editor_pick,
                "sector_id": sector_id,
                "status": status,
                "impact": impact,
                "timeline_source": timeline_source,
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return self._get(
            "/api/qdata/v1/analysis/public_research",
            cast_to=PublicResearchListResponse,
            options={"params": params},
        )

    def create_market_research(
        self,
        *,
        body: ResearchCreateRequest | dict[str, Any],
    ) -> ResearchAggregateResponse:
        """Create one market research root, optionally bootstrapping its first result."""
        request = body if isinstance(body, ResearchCreateRequest) else model_validate(ResearchCreateRequest, body)
        return self._post(
            "/api/qdata/v1/analysis/research",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

    def update_market_research(self, research_uid: str, *, body: ResearchUpdateRequest | dict[str, Any]) -> ResearchAggregateResponse:
        """Update supplied root fields only; this does not append a research result."""
        request = body if isinstance(body, ResearchUpdateRequest) else model_validate(ResearchUpdateRequest, body)
        return self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_unset=True), "max_retries": 0},
        )

    def get_market_research(
        self,
        research_uid: str,
        *,
        result_content_fields: str | None = None,
    ) -> ResearchAggregateResponse:
        """Get one market research root with its latest result and effective timeline."""
        params = {"result_content_fields": result_content_fields} if result_content_fields is not None else {}
        return self._get(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchAggregateResponse,
            options={"params": params} if params else None,
        )

    def delete_market_research(self, research_uid: str) -> ResearchDeleteResponse:
        """Soft-delete one market research root."""
        return self._delete(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchDeleteResponse,
        )

    def list_market_research_results(
        self,
        research_uid: str,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResearchResultListResponse:
        """List market research results, newest first."""
        params = {
            key: value
            for key, value in {
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return self._get(
            f"/api/qdata/v1/analysis/research/{research_uid}/results",
            cast_to=ResearchResultListResponse,
            options={"params": params},
        )

    def create_market_research_result(
        self,
        research_uid: str,
        *,
        body: ResearchResultSnapshotRequest | dict[str, Any],
    ) -> ResearchResultWriteResponse:
        """Append once with HTML outcome and required non-blank outcome_markdown; never retry an uncertain write."""
        request = body if isinstance(body, ResearchResultSnapshotRequest) else model_validate(ResearchResultSnapshotRequest, body)
        return self._post(
            f"/api/qdata/v1/analysis/research/{research_uid}/results",
            cast_to=ResearchResultWriteResponse,
            # Explicit nulls are part of the producer contract and must be
            # retained in the server's producer_payload.
            options={"json": model_dump(request, exclude_none=False), "max_retries": 0},
        )

    def update_market_research_result(
        self,
        research_uid: str,
        result_id: int,
        *,
        body: ResearchResultSnapshotRequest | dict[str, Any],
    ) -> ResearchResultWriteResponse:
        """Correct a result with a complete snapshot. Keep its job_run_id unchanged."""
        request = body if isinstance(body, ResearchResultSnapshotRequest) else model_validate(ResearchResultSnapshotRequest, body)
        return self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}/results/{result_id}",
            cast_to=ResearchResultWriteResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

    def replace_market_research_timeline(
        self,
        research_uid: str,
        *,
        body: ResearchTimelineReplaceRequest | dict[str, Any],
    ) -> ResearchAggregateResponse:
        """Replace the effective timeline and select manual timeline ownership."""
        request = body if isinstance(body, ResearchTimelineReplaceRequest) else model_validate(ResearchTimelineReplaceRequest, body)
        return self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}/timeline",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

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

    def get_market_structured_events(
        self,
        *,
        id: int | None = None,
        event_uid: str | None = None,
        as_of_date: str | None = None,
        lookback_hours: float | None = None,
        market: str | None = None,
        family: str | None = None,
        kind_id: str | None = None,
        tier: str | None = None,
        event_time_from: str | None = None,
        event_time_to: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> MarketStructuredEventListResponse:
        """List structured market events."""
        params = {
            key: value
            for key, value in {
                "id": id,
                "event_uid": event_uid,
                "as_of_date": as_of_date,
                "lookback_hours": lookback_hours,
                "market": market,
                "family": family,
                "kind_id": kind_id,
                "tier": tier,
                "event_time_from": event_time_from,
                "event_time_to": event_time_to,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return self._get(
            "/api/qdata/v1/analysis/market_structured_events",
            cast_to=MarketStructuredEventListResponse,
            options={"params": params},
        )

    market_structured_events = get_market_structured_events

    def create_market_structured_events(
        self,
        *,
        body: MarketMacroEventDailyRequest | dict[str, Any],
    ) -> MarketStructuredEventIngestResponse:
        """Ingest structured market events."""
        request = body if isinstance(body, MarketMacroEventDailyRequest) else model_validate(MarketMacroEventDailyRequest, body)
        return self._post(
            "/api/qdata/v1/analysis/market_structured_events",
            cast_to=MarketStructuredEventIngestResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    def get_attribution_factor(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
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
        page : int, optional
            One-based result page.
        size : int, optional
            Records per page, at most 200.
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
            Deprecated compatibility limit. Use page and size instead.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
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
        start_date: str,
        page: int | None = None,
        size: int | None = None,
        market: str | None = None,
        sector_id: int | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> SectorBriefExtractListResponse:
        """List extracted sector briefs."""
        params = {
            key: value
            for key, value in {
                "page": page,
                "size": size,
                "market": market,
                "sector_id": sector_id,
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

    async def list_sector_l2_events(
        self,
        *,
        id: int | None = None,
        as_of_date: str | None = None,
        market: str | None = None,
        kind_id: str | None = None,
        signal_type: str | None = None,
        source_scope: str | None = None,
        sector_id: int | None = None,
        ticker: str | None = None,
        event_datetime_from: str | None = None,
        event_datetime_to: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorL2EventListResponse:
        """List sector L2 events asynchronously using the supported event filters."""
        request = model_validate(
            SectorL2EventListRequest,
            {
                "id": id,
                "as_of_date": as_of_date,
                "market": market,
                "kind_id": kind_id,
                "signal_type": signal_type,
                "source_scope": source_scope,
                "sector_id": sector_id,
                "ticker": ticker,
                "event_datetime_from": event_datetime_from,
                "event_datetime_to": event_datetime_to,
                "limit": limit,
                "offset": offset,
            },
        )
        return await self._get(
            "/api/qdata/v1/analysis/research/sector_l2_events",
            cast_to=SectorL2EventListResponse,
            options={"params": model_dump(request, mode="json", exclude_none=True)},
        )

    async def create_sector_l2_events(
        self,
        *,
        body: SectorL2EventCreateRequest | dict[str, Any],
    ) -> SectorL2EventCreateResponse:
        """Create sector L2 events asynchronously."""
        request = body if isinstance(body, SectorL2EventCreateRequest) else model_validate(SectorL2EventCreateRequest, body)
        return await self._post(
            "/api/qdata/v1/analysis/research/sector_l2_events",
            cast_to=SectorL2EventCreateResponse,
            options={"json": model_dump(request, mode="json")},
        )

    async def get_sector_l2_event(self, event_id: int) -> SectorL2EventResponse:
        """Get one sector L2 event by ID asynchronously."""
        return await self._get(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
        )

    async def update_sector_l2_event(
        self,
        event_id: int,
        *,
        body: SectorL2EventUpdateRequest | dict[str, Any],
    ) -> SectorL2EventResponse:
        """Partially update one sector L2 event asynchronously."""
        request = body if isinstance(body, SectorL2EventUpdateRequest) else model_validate(SectorL2EventUpdateRequest, body)
        return await self._put(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
            options={"json": model_dump(request, mode="json", exclude_unset=True)},
        )

    async def delete_sector_l2_event(self, event_id: int) -> SectorL2EventResponse:
        """Delete one sector L2 event asynchronously."""
        return await self._delete(
            f"/api/qdata/v1/analysis/research/sector_l2_events/{event_id}",
            cast_to=SectorL2EventResponse,
        )

    async def list_market_research(
        self,
        *,
        scope: Literal["public", "mine", "starred"] | None = None,
        is_editor_pick: bool | None = None,
        sector_id: int | None = None,
        status: str | None = None,
        impact: Literal["medium", "high", "severe"] | None = None,
        timeline_source: Literal["producer", "manual"] | None = None,
        visibility: Literal["private", "public"] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResearchListResponse:
        """List roots asynchronously, optionally selecting public, mine, or starred."""
        params = {
            key: value
            for key, value in {
                "scope": scope,
                "is_editor_pick": is_editor_pick,
                "sector_id": sector_id,
                "status": status,
                "impact": impact,
                "timeline_source": timeline_source,
                "visibility": visibility,
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return await self._get(
            "/api/qdata/v1/analysis/research",
            cast_to=ResearchListResponse,
            options={"params": params},
        )

    async def list_public_market_research(
        self,
        *,
        is_editor_pick: bool | None = None,
        sector_id: int | None = None,
        status: str | None = None,
        impact: Literal["medium", "high", "severe"] | None = None,
        timeline_source: Literal["producer", "manual"] | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PublicResearchListResponse:
        """List strictly public research; caller-owned private roots are never included."""
        params = {
            key: value
            for key, value in {
                "is_editor_pick": is_editor_pick,
                "sector_id": sector_id,
                "status": status,
                "impact": impact,
                "timeline_source": timeline_source,
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return await self._get(
            "/api/qdata/v1/analysis/public_research",
            cast_to=PublicResearchListResponse,
            options={"params": params},
        )

    async def create_market_research(
        self,
        *,
        body: ResearchCreateRequest | dict[str, Any],
    ) -> ResearchAggregateResponse:
        """Create one market research root, optionally bootstrapping its first result asynchronously."""
        request = body if isinstance(body, ResearchCreateRequest) else model_validate(ResearchCreateRequest, body)
        return await self._post(
            "/api/qdata/v1/analysis/research",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

    async def update_market_research(self, research_uid: str, *, body: ResearchUpdateRequest | dict[str, Any]) -> ResearchAggregateResponse:
        """Update supplied root fields only, without replaying a failed write."""
        request = body if isinstance(body, ResearchUpdateRequest) else model_validate(ResearchUpdateRequest, body)
        return await self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_unset=True), "max_retries": 0},
        )

    async def get_market_research(
        self,
        research_uid: str,
        *,
        result_content_fields: str | None = None,
    ) -> ResearchAggregateResponse:
        """Get one market research root with its latest result and effective timeline asynchronously."""
        params = {"result_content_fields": result_content_fields} if result_content_fields is not None else {}
        return await self._get(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchAggregateResponse,
            options={"params": params} if params else None,
        )

    async def delete_market_research(self, research_uid: str) -> ResearchDeleteResponse:
        """Soft-delete one market research root."""
        return await self._delete(
            f"/api/qdata/v1/analysis/research/{research_uid}",
            cast_to=ResearchDeleteResponse,
        )

    async def list_market_research_results(
        self,
        research_uid: str,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        fuzzy: str | None = None,
        result_content_fields: str | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> ResearchResultListResponse:
        """List market research results, newest first asynchronously."""
        params = {
            key: value
            for key, value in {
                "start_time": start_time,
                "end_time": end_time,
                "fuzzy": fuzzy,
                "result_content_fields": result_content_fields,
                "order_by": order_by,
                "order_type": order_type,
                "page": page,
                "size": size,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return await self._get(
            f"/api/qdata/v1/analysis/research/{research_uid}/results",
            cast_to=ResearchResultListResponse,
            options={"params": params},
        )

    async def create_market_research_result(
        self,
        research_uid: str,
        *,
        body: ResearchResultSnapshotRequest | dict[str, Any],
    ) -> ResearchResultWriteResponse:
        """Append once with HTML outcome and required non-blank outcome_markdown asynchronously, without retries."""
        request = body if isinstance(body, ResearchResultSnapshotRequest) else model_validate(ResearchResultSnapshotRequest, body)
        return await self._post(
            f"/api/qdata/v1/analysis/research/{research_uid}/results",
            cast_to=ResearchResultWriteResponse,
            options={"json": model_dump(request, exclude_none=False), "max_retries": 0},
        )

    async def update_market_research_result(
        self,
        research_uid: str,
        result_id: int,
        *,
        body: ResearchResultSnapshotRequest | dict[str, Any],
    ) -> ResearchResultWriteResponse:
        """Correct a result with a complete snapshot. Keep its job_run_id unchanged."""
        request = body if isinstance(body, ResearchResultSnapshotRequest) else model_validate(ResearchResultSnapshotRequest, body)
        return await self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}/results/{result_id}",
            cast_to=ResearchResultWriteResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

    async def replace_market_research_timeline(
        self,
        research_uid: str,
        *,
        body: ResearchTimelineReplaceRequest | dict[str, Any],
    ) -> ResearchAggregateResponse:
        """Replace the effective timeline and select manual timeline ownership asynchronously."""
        request = body if isinstance(body, ResearchTimelineReplaceRequest) else model_validate(ResearchTimelineReplaceRequest, body)
        return await self._put(
            f"/api/qdata/v1/analysis/research/{research_uid}/timeline",
            cast_to=ResearchAggregateResponse,
            options={"json": model_dump(request, exclude_none=False)},
        )

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

    async def get_market_structured_events(
        self,
        *,
        id: int | None = None,
        event_uid: str | None = None,
        as_of_date: str | None = None,
        lookback_hours: float | None = None,
        market: str | None = None,
        family: str | None = None,
        kind_id: str | None = None,
        tier: str | None = None,
        event_time_from: str | None = None,
        event_time_to: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> MarketStructuredEventListResponse:
        """List structured market events asynchronously."""
        params = {
            key: value
            for key, value in {
                "id": id,
                "event_uid": event_uid,
                "as_of_date": as_of_date,
                "lookback_hours": lookback_hours,
                "market": market,
                "family": family,
                "kind_id": kind_id,
                "tier": tier,
                "event_time_from": event_time_from,
                "event_time_to": event_time_to,
                "limit": limit,
                "offset": offset,
            }.items()
            if value is not None
        }
        return await self._get(
            "/api/qdata/v1/analysis/market_structured_events",
            cast_to=MarketStructuredEventListResponse,
            options={"params": params},
        )

    market_structured_events = get_market_structured_events

    async def create_market_structured_events(
        self,
        *,
        body: MarketMacroEventDailyRequest | dict[str, Any],
    ) -> MarketStructuredEventIngestResponse:
        """Ingest structured market events asynchronously."""
        request = body if isinstance(body, MarketMacroEventDailyRequest) else model_validate(MarketMacroEventDailyRequest, body)
        return await self._post(
            "/api/qdata/v1/analysis/market_structured_events",
            cast_to=MarketStructuredEventIngestResponse,
            options={"json": model_dump(request, exclude_none=True)},
        )

    async def get_attribution_factor(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
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
        """Retrieves attribution factor analysis data asynchronously.

        Parameters
        ----------
        page : int, optional
            One-based result page.
        size : int, optional
            Records per page, at most 200.
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
            Deprecated compatibility limit. Use page and size instead.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
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
        start_date: str,
        page: int | None = None,
        size: int | None = None,
        market: str | None = None,
        sector_id: int | None = None,
        end_date: str | None = None,
        limit: int | None = None,
    ) -> SectorBriefExtractListResponse:
        """List extracted sector briefs asynchronously."""
        params = {
            key: value
            for key, value in {
                "page": page,
                "size": size,
                "market": market,
                "sector_id": sector_id,
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
