from unittest.mock import AsyncMock, Mock

import pytest

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import MarketDynamicsCreateResponse

PAYLOAD = {
    "market": "cn",
    "trading_date": "2026-08-11",
    "event_time": "2026-08-11T09:30:00+08:00",
    "generation_time": "2026-08-11T01:45:00Z",
    "event_rank": "mainline",
    "confidence": "high",
    "driver_status": "verified",
    "index_evidence": "上证指数上涨",
    "event_summary": {"category": "geo_military"},
    "sector_impacts": [],
}


def test_create_market_dynamics_sends_market_and_trading_date() -> None:
    client = Mock()
    client.post.return_value = MarketDynamicsCreateResponse(data=[])

    Analysis(client).create_market_dynamics(**PAYLOAD)

    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/market_dynamics",
        cast_to=MarketDynamicsCreateResponse,
        options={"json": PAYLOAD},
    )


@pytest.mark.asyncio
async def test_create_market_dynamics_async_sends_market_and_trading_date() -> None:
    client = Mock()
    client.post = AsyncMock(return_value=MarketDynamicsCreateResponse(data=[]))

    await AsyncAnalysis(client).create_market_dynamics(**PAYLOAD)

    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/market_dynamics",
        cast_to=MarketDynamicsCreateResponse,
        options={"json": PAYLOAD},
    )
