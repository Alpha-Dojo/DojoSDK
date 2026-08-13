from __future__ import annotations

import pytest

from dojo.resources.base import normalize_naive_iso_datetime
from dojo.resources.benchmark import AsyncBenchmark, Benchmark


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


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("2026-08-10", "2026-08-10"),
        ("2026-08-10T00:00:00+08:00", "2026-08-10T00:00:00"),
        ("2026-08-10T00:00:00Z", "2026-08-10T00:00:00"),
    ],
)
def test_normalize_naive_iso_datetime_preserves_wall_time(raw, expected) -> None:
    assert normalize_naive_iso_datetime(raw) == expected


def test_sync_benchmark_kline_strips_timezone_from_query() -> None:
    client = SyncClient()
    Benchmark(client).get_kline(
        symbol="000001.SS",
        start_time="2026-08-10T00:00:00+08:00",
        end_time="2026-08-12T23:59:59Z",
    )
    assert client.options["params"]["start_time"] == "2026-08-10T00:00:00"
    assert client.options["params"]["end_time"] == "2026-08-12T23:59:59"


@pytest.mark.asyncio
async def test_async_benchmark_kline_strips_timezone_from_query() -> None:
    client = AsyncClient()
    await AsyncBenchmark(client).get_kline(
        symbol="000001.SS",
        start_time="2026-08-10T00:00:00+08:00",
        end_time="2026-08-12",
    )
    assert client.options["params"]["start_time"] == "2026-08-10T00:00:00"
    assert client.options["params"]["end_time"] == "2026-08-12"
