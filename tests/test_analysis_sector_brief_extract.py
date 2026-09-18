from unittest.mock import AsyncMock, Mock

import pytest
from pydantic import ValidationError

from dojo.resources.analysis import Analysis, AsyncAnalysis
from dojo.types.models import SectorBriefExtractListResponse, SectorBriefExtractWriteResponse

BODY = {
    "generation_time": "2026-09-18T03:28:40Z",
    "items": [
        {
            "market": "hk",
            "sector_ref": "177/178/181",
            "as_of_date": "2026-09-17",
            "key_drivers": [
                {
                    "title": {"zh": "需求改善", "en": "Demand improves"},
                    "importance": "high",
                    "price_direction": "up",
                }
            ],
            "key_risks": [],
            "top_components": [
                {
                    "ticker": "00981.HK",
                    "role_label": {"zh": "晶圆代工", "en": "Foundry"},
                    "thesis": {"zh": "订单改善", "en": "Orders improve"},
                }
            ],
        }
    ],
}


def test_create_sector_brief_extract_accepts_sector_ref() -> None:
    client = Mock()
    expected = SectorBriefExtractWriteResponse(data=[], receipt={"succeeded_count": 1, "failed_count": 0})
    client.post.return_value = expected

    result = Analysis(client).create_sector_brief_extract(body=BODY)

    assert result is expected
    client.post.assert_called_once_with(
        "/api/qdata/v1/analysis/sector_brief_extract",
        cast_to=SectorBriefExtractWriteResponse,
        options={"json": BODY},
    )


@pytest.mark.asyncio
async def test_create_sector_brief_extract_async_accepts_sector_ref() -> None:
    client = Mock()
    client.post = AsyncMock(return_value=SectorBriefExtractWriteResponse(data=[]))

    await AsyncAnalysis(client).create_sector_brief_extract(body=BODY)

    client.post.assert_awaited_once_with(
        "/api/qdata/v1/analysis/sector_brief_extract",
        cast_to=SectorBriefExtractWriteResponse,
        options={"json": BODY},
    )


def test_create_sector_brief_extract_requires_sector_ref() -> None:
    client = Mock()
    invalid = {**BODY, "items": [{key: value for key, value in BODY["items"][0].items() if key != "sector_ref"}]}

    with pytest.raises(ValidationError, match="sector_ref"):
        Analysis(client).create_sector_brief_extract(body=invalid)

    client.post.assert_not_called()


def test_list_sector_brief_extract_sends_pagination() -> None:
    client = Mock()
    expected = SectorBriefExtractListResponse(page=2, size=200, total_num=201, total_page=2, num=1, data=[])
    client.get.return_value = expected

    result = Analysis(client).list_sector_brief_extract(start_date="2026-09-01", page=2, size=200, market="hk")

    assert result is expected
    client.get.assert_called_once_with(
        "/api/qdata/v1/analysis/sector_brief_extract",
        cast_to=SectorBriefExtractListResponse,
        options={"params": {"page": 2, "size": 200, "market": "hk", "start_date": "2026-09-01"}},
    )


@pytest.mark.asyncio
async def test_list_sector_brief_extract_async_sends_pagination() -> None:
    client = Mock()
    expected = SectorBriefExtractListResponse(page=2, size=200, total_num=201, total_page=2, num=1, data=[])
    client.get = AsyncMock(return_value=expected)

    result = await AsyncAnalysis(client).list_sector_brief_extract(start_date="2026-09-01", page=2, size=200, market="hk")

    assert result is expected
    client.get.assert_awaited_once_with(
        "/api/qdata/v1/analysis/sector_brief_extract",
        cast_to=SectorBriefExtractListResponse,
        options={"params": {"page": 2, "size": 200, "market": "hk", "start_date": "2026-09-01"}},
    )
