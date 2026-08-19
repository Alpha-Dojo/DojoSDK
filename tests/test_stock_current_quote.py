from __future__ import annotations

import httpx
import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo


def _response() -> dict:
    return {
        "message": "",
        "code": 0,
        "data": {"total_num": 1, "data": [{"symbol": "AAPL", "last_price": 200.0}]},
    }


def test_sync_current_quote_uses_comma_separated_symbols(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_response())

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        response = client.stocks.get_quote(symbols=["AAPL", "MSFT", "600519.SH"])
    finally:
        http_client.close()

    assert seen[0].url.params.get_list("symbols") == ["AAPL,MSFT,600519.SH"]
    assert response == _response()["data"]


@pytest.mark.asyncio
async def test_async_current_quote_uses_comma_separated_symbols(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_response())

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", http_client=http_client)
    try:
        response = await client.stocks.get_quote(symbols=["AAPL", "MSFT", "600519.SH"])
    finally:
        await http_client.aclose()

    assert seen[0].url.params.get_list("symbols") == ["AAPL,MSFT,600519.SH"]
    assert response == _response()["data"]
