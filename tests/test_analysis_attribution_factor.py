from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import AttributionFactorWriteResponse

BODY = {
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
    ]
}


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
