from __future__ import annotations

import pytest

from dojo.resources.sectors import AsyncSectors, Sectors


class SyncClient:
    def __init__(self) -> None:
        self.options = None

    def get(self, _path, *, cast_to, options):
        del cast_to
        self.options = options
        return {}


class AsyncClient:
    def __init__(self) -> None:
        self.options = None

    async def get(self, _path, *, cast_to, options):
        del cast_to
        self.options = options
        return {}


def test_sync_sector_info_forwards_version() -> None:
    client = SyncClient()
    Sectors(client).get_info(version="2026.09")
    assert client.options["params"] == {"version": "2026.09"}


@pytest.mark.asyncio
async def test_async_sector_info_forwards_version() -> None:
    client = AsyncClient()
    await AsyncSectors(client).get_info(version="2026.09")
    assert client.options["params"] == {"version": "2026.09"}
