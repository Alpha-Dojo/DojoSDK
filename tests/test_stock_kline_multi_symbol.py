from __future__ import annotations

import httpx
import pandas as pd
import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo
from dojo.datasource.huggingface import HuggingFaceKlineDataSource
from dojo.types.models import StockKlineResponse, StockKlineResponseItem

CURL_PAYLOAD = {
    "total_num": 2,
    "data": {
        "NVDA": [
            {
                "bar_time": "2026-07-21T00:00:00",
                "open": 207.3080287924173,
                "high": 208.41678812536318,
                "low": 203.78197433719308,
                "close": 207.058308221934,
                "vol": 108685563.0,
                "amount": 22436488656.0,
                "tr": 0.45,
                "change_p": 1.9726485635576552,
                "adj_factor_cum": 43.679698264243044,
                "dividends": 0,
                "splits": 0,
                "kline_t": "1D",
            },
            {
                "bar_time": "2026-07-20T00:00:00",
                "open": 205.63989538158887,
                "high": 207.50780524880395,
                "low": 202.05390798944865,
                "close": 203.05279027138187,
                "vol": 88701540.0,
                "amount": 18148030474.0,
                "tr": 0.37,
                "change_p": 0.23174399684433578,
                "adj_factor_cum": 43.679698264243044,
                "dividends": 0,
                "splits": 0,
                "kline_t": "1D",
            },
        ],
        "AAPL": [
            {
                "bar_time": "2026-07-21T00:00:00",
                "open": 322.851555229311,
                "high": 329.31597995723365,
                "low": 321.94233938658925,
                "close": 327.45758274024195,
                "vol": 41338917.0,
                "amount": 13515902582.0,
                "tr": 0.28,
                "change_p": 0.3521234575461607,
                "adj_factor_cum": 33.40523327178309,
                "dividends": 0,
                "splits": 0,
                "kline_t": "1D",
            },
            {
                "bar_time": "2026-07-20T00:00:00",
                "open": 333.2226106660709,
                "high": 333.42243832381195,
                "low": 323.40108128809885,
                "close": 326.30857370823094,
                "vol": 53468008.0,
                "amount": 17479885376.0,
                "tr": 0.36,
                "change_p": -2.14238628872776,
                "adj_factor_cum": 33.40523327178309,
                "dividends": 0,
                "splits": 0,
                "kline_t": "1D",
            },
        ],
    },
}

SINGLE_PAYLOAD = {
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


def test_stock_kline_model_single_symbol():
    res = StockKlineResponse.model_validate(SINGLE_PAYLOAD)
    assert res.total_num == 1
    assert isinstance(res.data, list)
    assert len(res.data) == 1
    assert res.data[0].symbol == "AAPL"
    assert res.data[0].close == 327.45


def test_stock_kline_model_multi_symbol():
    res = StockKlineResponse.model_validate(CURL_PAYLOAD)
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "NVDA" in res.data and "AAPL" in res.data
    assert len(res.data["NVDA"]) == 2
    assert len(res.data["AAPL"]) == 2
    assert res.data["NVDA"][0].close == 207.058308221934
    assert res.data["NVDA"][0].bar_time == "2026-07-21T00:00:00"
    assert res.data["AAPL"][0].close == 327.45758274024195


def test_client_get_kline_multi_symbol_comma_separated(monkeypatch):
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": CURL_PAYLOAD})

    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = client.stocks.get_kline(symbol="AAPL,NVDA", kline_t="1D", limit=1000)
    finally:
        http_client.close()

    assert len(captured) == 1
    assert dict(captured[0].url.params)["symbol"] == "AAPL,NVDA"
    assert response.total_num == 2
    assert isinstance(response.data, dict)
    assert "NVDA" in response.data


def test_client_get_kline_multi_symbol_list(monkeypatch):
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": CURL_PAYLOAD})

    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = client.stocks.get_kline(symbol=["AAPL", "NVDA"], kline_t="1D", limit=1000)
    finally:
        http_client.close()

    assert len(captured) == 1
    assert dict(captured[0].url.params)["symbol"] == "AAPL,NVDA"
    assert response.total_num == 2
    assert isinstance(response.data, dict)


@pytest.mark.asyncio
async def test_async_client_get_kline_multi_symbol_list(monkeypatch):
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": CURL_PAYLOAD})

    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        response = await client.stocks.get_kline(symbol=["AAPL", "NVDA"], kline_t="1D", limit=1000)
    finally:
        await http_client.aclose()

    assert len(captured) == 1
    assert dict(captured[0].url.params)["symbol"] == "AAPL,NVDA"
    assert response.total_num == 2
    assert isinstance(response.data, dict)


def test_get_all_klines_flattens_multi_symbol_dict(monkeypatch):
    monkeypatch.setenv("DOJO_ONLINE", "false")
    client = Dojo(api_key="test", return_raw_data=False)

    class MockOfflineSource:
        def fetch(self, **_kwargs):
            return {"message": "ok", "code": 0, "data": CURL_PAYLOAD}

    client._data_source = MockOfflineSource()
    klines = client.stocks.get_all_klines(symbols=["AAPL", "NVDA"])
    assert isinstance(klines, list)
    assert len(klines) == 4
    assert all(isinstance(item, StockKlineResponseItem) for item in klines)


def test_offline_huggingface_kline_multi_symbol_grouping(monkeypatch):
    ds = HuggingFaceKlineDataSource()

    df = pd.DataFrame(
        [
            {"symbol": "AAPL", "bar_time": "2026-07-20T00:00:00", "close": 326.3, "kline_t": "1D"},
            {"symbol": "AAPL", "bar_time": "2026-07-21T00:00:00", "close": 327.4, "kline_t": "1D"},
            {"symbol": "NVDA", "bar_time": "2026-07-20T00:00:00", "close": 203.0, "kline_t": "1D"},
            {"symbol": "NVDA", "bar_time": "2026-07-21T00:00:00", "close": 207.0, "kline_t": "1D"},
        ]
    )

    monkeypatch.setattr(ds, "fetch_df", lambda path: df)

    # 1. Single symbol -> list
    res_single = ds.fetch(method="GET", path="/api/qdata/v1/stock/kline", params={"symbol": "AAPL"})
    assert res_single["code"] == 0
    assert res_single["data"]["total_num"] == 2
    assert isinstance(res_single["data"]["data"], list)

    # 2. Multi symbol -> dict
    res_multi = ds.fetch(method="GET", path="/api/qdata/v1/stock/kline", params={"symbol": "AAPL,NVDA"})
    assert res_multi["code"] == 0
    assert res_multi["data"]["total_num"] == 2
    assert isinstance(res_multi["data"]["data"], dict)
    assert "AAPL" in res_multi["data"]["data"]
    assert "NVDA" in res_multi["data"]["data"]
    assert len(res_multi["data"]["data"]["AAPL"]) == 2
    assert len(res_multi["data"]["data"]["NVDA"]) == 2
