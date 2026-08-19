from __future__ import annotations

import httpx
import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo

KLINE_PAYLOAD = {
    "total_num": 1,
    "data": [
        {
            "symbol": "AAPL",
            "kline_t": "1D",
            "bar_time": "2026-07-21T00:00:00",
            "open": 322.85,
            "high": 329.31,
            "low": 321.94,
            "close": 327.45,
            "vol": 41338917.0,
        }
    ],
}


def _handler(request: httpx.Request) -> httpx.Response:
    return httpx.Response(200, json={"message": "", "code": 0, "data": KLINE_PAYLOAD})


def test_sync_stock_kline_preserves_online_data_contract(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(_handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = client.stocks.get_kline(symbol="AAPL", kline_t="1D")
    finally:
        http_client.close()

    assert response.total_num == 1
    assert response.data[0].symbol == "AAPL"
    assert not hasattr(response, "klines")


def test_sync_stock_kline_online_and_offline_have_same_shape(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(_handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)

    class OfflineSource:
        def fetch(self, **_kwargs):
            return {"message": "ok", "code": 0, "data": KLINE_PAYLOAD}

    try:
        online = client.stocks.get_kline(symbol="AAPL", kline_t="1D")
        client._online = False
        client._data_source = OfflineSource()
        offline = client.stocks.get_kline(symbol="AAPL", kline_t="1D")
    finally:
        http_client.close()

    assert online.model_dump() == offline.model_dump()
    assert set(offline.model_dump()) == {"total_num", "data"}


def test_generic_market_kline_uses_data_not_klines(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(_handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = client.market_data.get_kline(exchange="nasdaq", bz_type="stock", symbol="AAPL")
    finally:
        http_client.close()

    assert response.total_num == 1
    assert response.data[0]["symbol"] == "AAPL"
    assert not hasattr(response, "klines")


@pytest.mark.asyncio
async def test_async_benchmark_kline_preserves_online_data_contract(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(_handler))
    client = AsyncDojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = await client.benchmark.get_kline(symbol="SPX", kline_t="1D")
    finally:
        await http_client.aclose()

    assert response.total_num == 1
    assert response.data[0]["symbol"] == "AAPL"
    assert not hasattr(response, "klines")
