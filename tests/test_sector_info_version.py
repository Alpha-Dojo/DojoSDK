from unittest.mock import AsyncMock, Mock

import pytest

from dojo.resources.sectors import AsyncSectors, Sectors
from dojo.types.models import SectorInfoListResponse


def test_get_info_sends_taxonomy_version() -> None:
    client = Mock()
    client.get.return_value = SectorInfoListResponse(total_num=0, data=[])

    Sectors(client).get_info(version="v2", tree=True)

    client.get.assert_called_once_with(
        "/api/qdata/v1/sector/info",
        cast_to=SectorInfoListResponse,
        options={"params": {"version": "v2", "tree": True}},
    )


@pytest.mark.asyncio
async def test_get_info_async_sends_taxonomy_version() -> None:
    client = Mock()
    client.get = AsyncMock(return_value=SectorInfoListResponse(total_num=0, data=[]))

    await AsyncSectors(client).get_info(version="v2", tree=True)

    client.get.assert_awaited_once_with(
        "/api/qdata/v1/sector/info",
        cast_to=SectorInfoListResponse,
        options={"params": {"version": "v2", "tree": True}},
    )
