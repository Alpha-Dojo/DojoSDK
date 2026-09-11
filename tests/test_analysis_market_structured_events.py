from unittest.mock import AsyncMock, Mock

import pytest

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import (
    MarketStructuredEventIngestResponse,
    MarketStructuredEventListResponse,
)

PARAMS = {
    "id": 7,
    "event_uid": "evt-7",
    "as_of_date": "2026-09-11",
    "lookback_hours": 24.0,
    "market": "cn",
    "family": "macro",
    "kind_id": "policy",
    "tier": "major",
    "event_time_from": "2026-09-10T00:00:00",
    "event_time_to": "2026-09-11T00:00:00",
    "limit": 100,
    "offset": 10,
}

BODY = {
    "schema_version": "market-macro-event-daily.v1",
    "task_name": "daily-market-events",
    "as_of_date": "2026-09-11",
    "lookback_hours": 24,
    "coverage": {"markets": ["cn"]},
    "events": [],
}


def test_get_market_structured_events_sends_openapi_parameters() -> None:
    client = Mock()
    client.get.return_value = MarketStructuredEventListResponse(total_num=0, data=[])

    Analysis(client).get_market_structured_events(**PARAMS)

    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/market_structured_events",
        cast_to=MarketStructuredEventListResponse,
        options={"params": PARAMS},
    )


@pytest.mark.asyncio
async def test_get_market_structured_events_async_sends_openapi_parameters() -> None:
    client = Mock()
    client.get = AsyncMock(return_value=MarketStructuredEventListResponse(total_num=0, data=[]))

    await AsyncAnalysis(client).get_market_structured_events(**PARAMS)

    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/market_structured_events",
        cast_to=MarketStructuredEventListResponse,
        options={"params": PARAMS},
    )


def test_create_market_structured_events_validates_and_sends_body() -> None:
    client = Mock()
    client.post.return_value = MarketStructuredEventIngestResponse(accepted_event_count=0, event_uids=[])

    Analysis(client).create_market_structured_events(body=BODY)

    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/market_structured_events",
        cast_to=MarketStructuredEventIngestResponse,
        options={"json": BODY},
    )


@pytest.mark.asyncio
async def test_create_market_structured_events_async_validates_and_sends_body() -> None:
    client = Mock()
    client.post = AsyncMock(return_value=MarketStructuredEventIngestResponse(accepted_event_count=0, event_uids=[]))

    await AsyncAnalysis(client).create_market_structured_events(body=BODY)

    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/market_structured_events",
        cast_to=MarketStructuredEventIngestResponse,
        options={"json": BODY},
    )
