from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import AttributionFactorResponse, AttributionFactorWriteResponse

BODY = {
    "generation_time": "2026-08-11T01:45:00Z",
    "items": [
        {
            "claim": {"zh": "盈利增长", "en": "Earnings growth"},
            "sector_id": "technology",
            "market": "us",
            "factor_topic": "earnings",
            "evidence": [{"quote": "Revenue increased"}],
            "affected_tickers": ["AAPL"],
            "role": "explains_move",
            "payload_status": "ready",
        }
    ],
}


def test_get_attribution_factor_sends_pagination() -> None:
    client = Mock()
    expected = AttributionFactorResponse(page=2, size=200, total_num=201, total_page=2, num=1, data=[])
    client.get.return_value = expected

    result = Analysis(client).get_attribution_factor(page=2, size=200, market="cn")

    assert result is expected
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/attribution_factor",
        cast_to=AttributionFactorResponse,
        options={"params": {"page": 2, "size": 200, "market": "cn"}},
    )


@pytest.mark.asyncio
async def test_get_attribution_factor_async_sends_pagination() -> None:
    client = Mock()
    expected = AttributionFactorResponse(page=2, size=200, total_num=201, total_page=2, num=1, data=[])
    client.get = AsyncMock(return_value=expected)

    result = await AsyncAnalysis(client).get_attribution_factor(page=2, size=200, market="cn")

    assert result is expected
    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/attribution_factor",
        cast_to=AttributionFactorResponse,
        options={"params": {"page": 2, "size": 200, "market": "cn"}},
    )


def test_create_attribution_factor() -> None:
    client = Mock()
    expected = AttributionFactorWriteResponse(data=[])
    client.post.return_value = expected

    result = Analysis(client).create_attribution_factor(body=BODY)

    assert result is expected
    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/attribution_factor",
        cast_to=AttributionFactorWriteResponse,
        options={"json": BODY},
    )

    client.reset_mock()
    with pytest.raises(ValidationError):
        Analysis(client).create_attribution_factor(
            body={
                "items": [
                    {
                        "claim": {"zh": "盈利增长", "en": "Earnings growth"},
                        "sector_id": "",
                        "market": "us",
                        "factor_topic": "earnings",
                    }
                ]
            }
        )
    client.post.assert_not_called()


@pytest.mark.asyncio
async def test_create_attribution_factor_async() -> None:
    client = Mock()
    expected = AttributionFactorWriteResponse(data=[])
    client.post = AsyncMock(return_value=expected)

    result = await AsyncAnalysis(client).create_attribution_factor(body=BODY)

    assert result is expected
    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/attribution_factor",
        cast_to=AttributionFactorWriteResponse,
        options={"json": BODY},
    )
