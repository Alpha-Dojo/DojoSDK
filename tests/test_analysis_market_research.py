from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import (
    ResearchAggregateResponse,
    ResearchListResponse,
    ResearchResultListResponse,
    ResearchResultWriteResponse,
)


RESULT_BODY = {
    "task_name": "research-result",
    "observation_window": {"start_date": "2026-09-14", "end_date": "2026-09-28"},
    "probability_tier": None,
    "probability_pct": None,
    "outcome": "Evidence is currently insufficient for a reliable probability.",
    "timeline": [],
    "used_event_uids": [],
    "generation_time": "2026-09-14T10:00:00Z",
    "job_run_id": "job-20260914-001",
}

ROOT_BODY = {
    "research_uid": "research-energy-2026-001",
    "title": "Will the energy supply constraint ease?",
    "description": "Curated research metadata.",
    "observation_window": {"start_date": "2026-09-14", "end_date": "2026-09-28"},
    "sector_id": 42,
    "status": "tracking",
    "impact": "high",
    "visibility": "public",
    "timeline_source": "producer",
    "initial_result": RESULT_BODY,
}


def test_market_research_sync_routes_and_preserves_nullable_result_fields() -> None:
    client = Mock()
    client.get.return_value = ResearchListResponse(page=1, size=10, total_num=0, total_page=0, num=0, data=[])
    client.post.return_value = ResearchResultWriteResponse(result_id=901)

    Analysis(client).list_market_research(scope="all", sector_id=42, status="tracking", limit=25, offset=5)
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={"params": {"scope": "all", "sector_id": 42, "status": "tracking", "limit": 25, "offset": 5}},
    )

    client.reset_mock()
    result = Analysis(client).create_market_research_result(
        "research-energy-2026-001",
        body=RESULT_BODY,
    )

    assert result.result_id == 901
    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}},
    )


def test_market_research_sync_root_result_and_timeline_methods() -> None:
    client = Mock()
    client.post.return_value = ResearchAggregateResponse.model_validate(
        {
            **ROOT_BODY,
            "owner_user_id": "producer-admin",
            "latest_result": None,
            "latest_probability_tier": None,
            "latest_probability_pct": None,
            "related_sector": None,
            "extra": {},
            "timeline": [],
        }
    )
    client.get.return_value = ResearchAggregateResponse.model_validate(
        {
            **ROOT_BODY,
            "owner_user_id": "producer-admin",
            "latest_result": None,
            "latest_probability_tier": None,
            "latest_probability_pct": None,
            "related_sector": None,
            "extra": {},
            "timeline": [],
        }
    )
    client.put.return_value = client.post.return_value

    analysis = Analysis(client)
    analysis.create_market_research(body=ROOT_BODY)
    client.post.assert_called_once()
    assert client.post.call_args.args[0] == "/api/qdata/v1/analysis/research"
    assert client.post.call_args.kwargs["cast_to"] is ResearchAggregateResponse
    assert client.post.call_args.kwargs["options"]["json"]["initial_result"]["probability_pct"] is None

    analysis.get_market_research(ROOT_BODY["research_uid"])
    client.get.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001",
        cast_to=ResearchAggregateResponse,
        options={},
    )

    analysis.list_market_research_results(ROOT_BODY["research_uid"], limit=10, offset=20)
    client.get.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultListResponse,
        options={"params": {"limit": 10, "offset": 20}},
    )

    analysis.replace_market_research_timeline(ROOT_BODY["research_uid"], body={"items": []})
    client.put.assert_called_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/timeline",
        cast_to=ResearchAggregateResponse,
        options={"json": {"items": []}},
    )


def test_market_research_result_rejects_legacy_wire_fields() -> None:
    client = Mock()

    with pytest.raises(ValidationError):
        Analysis(client).create_market_research_result(
            "research-energy-2026-001",
            body={**RESULT_BODY, "decision_logic": "legacy"},
        )

    client.post.assert_not_called()


def test_market_research_sync_list_forwards_query_contract() -> None:
    client = Mock()
    client.get.return_value = ResearchListResponse(page=2, size=3, total_num=4, total_page=2, num=1, data=[])

    Analysis(client).list_market_research(
        scope="public",
        sector_id=42,
        status="tracking",
        start_time="2026-09-01",
        end_time="2026-09-30",
        fuzzy="resolve",
        order_by="title",
        order_type="asc",
        page=2,
        size=3,
    )

    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={
            "params": {
                "scope": "public",
                "sector_id": 42,
                "status": "tracking",
                "start_time": "2026-09-01",
                "end_time": "2026-09-30",
                "fuzzy": "resolve",
                "order_by": "title",
                "order_type": "asc",
                "page": 2,
                "size": 3,
            }
        },
    )

    client.reset_mock()
    client.get.return_value = ResearchResultListResponse(page=1, size=5, total_num=0, total_page=0, num=0, data=[])
    Analysis(client).list_market_research_results(
        "research-energy-2026-001",
        start_time="2026-09-01T00:00:00Z",
        end_time="2026-09-30T00:00:00+00:00",
        fuzzy="evidence",
        order_by="task_name",
        order_type="asc",
        page=1,
        size=5,
    )
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultListResponse,
        options={
            "params": {
                "start_time": "2026-09-01T00:00:00Z",
                "end_time": "2026-09-30T00:00:00+00:00",
                "fuzzy": "evidence",
                "order_by": "task_name",
                "order_type": "asc",
                "page": 1,
                "size": 5,
            }
        },
    )


@pytest.mark.asyncio
async def test_market_research_async_result_matches_sync_wire_contract() -> None:
    client = Mock()
    client.post = AsyncMock(return_value=ResearchResultWriteResponse(result_id=901))

    result = await AsyncAnalysis(client).create_market_research_result(
        "research-energy-2026-001",
        body=RESULT_BODY,
    )

    assert result.result_id == 901
    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}},
    )


@pytest.mark.asyncio
async def test_market_research_async_root_and_list_routes() -> None:
    client = Mock()
    client.get = AsyncMock(return_value=ResearchListResponse(page=1, size=10, total_num=0, total_page=0, num=0, data=[]))
    client.post = AsyncMock(return_value=ResearchResultWriteResponse(result_id=901))
    client.put = AsyncMock()

    analysis = AsyncAnalysis(client)
    await analysis.list_market_research(scope="all")
    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research",
        cast_to=ResearchListResponse,
        options={"params": {"scope": "all"}},
    )

    await analysis.create_market_research_result(ROOT_BODY["research_uid"], body=RESULT_BODY)
    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/research/research-energy-2026-001/results",
        cast_to=ResearchResultWriteResponse,
        options={"json": {**RESULT_BODY, "research_uid": None, "extra": {}}},
    )
