from __future__ import annotations

import httpx
import pandas as pd
import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo
from dojo.datasource.huggingface import HuggingFaceKlineDataSource, StockDataSource
from dojo.types.models import (
    BenchmarkKlineResponse,
    BenchmarkKLineResponse,
    StockFinIndicatorsResponse,
)

# Sample payloads
SAMPLE_FIN_INDICATORS_SINGLE = {
    "total_num": 1,
    "data": [
        {
            "report_type": "accumulate",
            "report_date": "2026-06-27 00:00:00",
            "public_date": "2026-07-31 00:00:00",
            "security_name": "苹果",
            "roa": 27.33011,
            "currency": "USD",
        }
    ],
}

SAMPLE_FIN_INDICATORS_MULTI = {
    "total_num": 2,
    "data": {
        "AAPL": [
            {
                "report_type": "accumulate",
                "report_date": "2026-06-27 00:00:00",
                "public_date": "2026-07-31 00:00:00",
                "security_name": "苹果",
                "roa": 27.33011,
                "currency": "USD",
            }
        ],
        "NVDA": [
            {
                "report_type": "accumulate",
                "report_date": "2026-07-28 00:00:00",
                "public_date": "2026-08-28 00:00:00",
                "security_name": "英伟达",
                "roa": 50.12345,
                "currency": "USD",
            }
        ],
    },
}

SAMPLE_BENCHMARK_KLINE_SINGLE = {
    "total_num": 1,
    "data": [
        {
            "symbol": "000001.SS",
            "bar_time": "2026-09-17 00:00:00",
            "open": 3877.0,
            "high": 3898.84,
            "low": 3866.89,
            "close": 3896.65,
            "vol": 472146900.0,
            "amount": 718228300000.0,
            "change_p": 0.4444,
            "adj_factor_cum": 1.0,
            "dividends": 0.0,
            "splits": 0.0,
            "kline_t": "1D",
        }
    ],
}

SAMPLE_BENCHMARK_KLINE_MULTI = {
    "total_num": 2,
    "data": {
        "000001.SS": [
            {
                "bar_time": "2026-09-17 00:00:00",
                "open": 3877.0,
                "high": 3898.84,
                "low": 3866.89,
                "close": 3896.65,
                "vol": 472146900.0,
                "amount": 718228300000.0,
                "change_p": 0.4444,
                "adj_factor_cum": 1.0,
                "dividends": 0.0,
                "splits": 0.0,
                "kline_t": "1D",
            }
        ],
        "^SPX": [
            {
                "bar_time": "2026-04-28 00:00:00",
                "open": 7133.74,
                "high": 7152.52,
                "low": 7115.17,
                "close": 7138.80,
                "vol": 4900650000.0,
                "amount": 0.0,
                "change_p": -0.489,
                "adj_factor_cum": 1.0,
                "dividends": 0.0,
                "splits": 0.0,
                "kline_t": "1D",
            }
        ],
    },
}


# ==========================================
# 1. Model Validation Tests
# ==========================================


def test_stock_fin_indicators_response_single_symbol() -> None:
    res = StockFinIndicatorsResponse.model_validate(SAMPLE_FIN_INDICATORS_SINGLE)
    assert res.total_num == 1
    assert isinstance(res.data, list)
    assert len(res.data) == 1
    assert res.data[0]["security_name"] == "苹果"
    assert res.data[0]["roa"] == 27.33011


def test_stock_fin_indicators_response_multi_symbol() -> None:
    res = StockFinIndicatorsResponse.model_validate(SAMPLE_FIN_INDICATORS_MULTI)
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "AAPL" in res.data
    assert "NVDA" in res.data
    assert res.data["AAPL"][0]["security_name"] == "苹果"
    assert res.data["NVDA"][0]["security_name"] == "英伟达"


def test_benchmark_kline_response_single_symbol() -> None:
    res = BenchmarkKLineResponse.model_validate(SAMPLE_BENCHMARK_KLINE_SINGLE)
    assert res.total_num == 1
    assert isinstance(res.data, list)
    assert len(res.data) == 1
    assert res.data[0]["symbol"] == "000001.SS"
    assert res.data[0]["close"] == 3896.65

    # Alias check
    res_alias = BenchmarkKlineResponse.model_validate(SAMPLE_BENCHMARK_KLINE_SINGLE)
    assert res_alias.total_num == 1


def test_benchmark_kline_response_multi_symbol() -> None:
    res = BenchmarkKLineResponse.model_validate(SAMPLE_BENCHMARK_KLINE_MULTI)
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "000001.SS" in res.data
    assert "^SPX" in res.data
    assert res.data["000001.SS"][0]["close"] == 3896.65
    assert res.data["^SPX"][0]["open"] == 7133.74


# ==========================================
# 2. Sync Client Resource Tests
# ==========================================


def test_sync_stocks_get_fin_indicators_multi_symbol_list(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_FIN_INDICATORS_MULTI})

    client = Dojo(api_key="test", return_raw_data=False, http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    res = client.stocks.get_fin_indicators(symbol=["AAPL", "NVDA"], limit=5)

    assert len(captured) == 1
    assert "symbol=AAPL%2CNVDA" in str(captured[0].url) or "symbol=AAPL,NVDA" in str(captured[0].url)
    assert "limit=5" in str(captured[0].url)
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "AAPL" in res.data
    assert "NVDA" in res.data


def test_sync_stocks_get_fin_indicators_multi_symbol_string(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_FIN_INDICATORS_MULTI})

    client = Dojo(api_key="test", return_raw_data=False, http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    res = client.stocks.get_fin_indicators(symbol="AAPL,NVDA")

    assert len(captured) == 1
    assert "symbol=AAPL%2CNVDA" in str(captured[0].url) or "symbol=AAPL,NVDA" in str(captured[0].url)
    assert isinstance(res.data, dict)


def test_sync_benchmark_get_kline_multi_symbol_list(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_BENCHMARK_KLINE_MULTI})

    client = Dojo(api_key="test", return_raw_data=False, http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    res = client.benchmark.get_kline(symbol=["000001.SS", "^SPX"], kline_t="1D", limit=100)

    assert len(captured) == 1
    url_str = str(captured[0].url)
    assert "000001.SS" in url_str and ("%5ESPX" in url_str or "^SPX" in url_str)
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "000001.SS" in res.data
    assert "^SPX" in res.data


def test_sync_benchmark_get_kline_multi_symbol_string(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_BENCHMARK_KLINE_MULTI})

    client = Dojo(api_key="test", return_raw_data=False, http_client=httpx.Client(transport=httpx.MockTransport(handler)))
    res = client.benchmark.get_kline(symbol="000001.SS,^SPX", kline_t="1D")

    assert len(captured) == 1
    assert res.total_num == 2
    assert isinstance(res.data, dict)


# ==========================================
# 3. Async Client Resource Tests
# ==========================================


@pytest.mark.asyncio
async def test_async_stocks_get_fin_indicators_multi_symbol(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_FIN_INDICATORS_MULTI})

    client = AsyncDojo(api_key="test", return_raw_data=False, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    res = await client.stocks.get_fin_indicators(symbol=["AAPL", "NVDA"])

    assert len(captured) == 1
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "AAPL" in res.data


@pytest.mark.asyncio
async def test_async_benchmark_get_kline_multi_symbol(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    captured: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        captured.append(request)
        return httpx.Response(200, json={"message": "", "code": 0, "data": SAMPLE_BENCHMARK_KLINE_MULTI})

    client = AsyncDojo(api_key="test", return_raw_data=False, http_client=httpx.AsyncClient(transport=httpx.MockTransport(handler)))
    res = await client.benchmark.get_kline(symbol=["000001.SS", "^SPX"], kline_t="1D")

    assert len(captured) == 1
    assert res.total_num == 2
    assert isinstance(res.data, dict)
    assert "000001.SS" in res.data


# ==========================================
# 4. Offline Datasource Tests
# ==========================================


def test_offline_stock_datasource_fin_indicators_multi_symbol(monkeypatch) -> None:
    ds = StockDataSource()

    # Mock super().fetch to return simulated flat parquet rows
    def mock_super_fetch(self, *, method, path, params, json=None):
        return {
            "code": 0,
            "message": "ok",
            "data": {
                "total_num": 4,
                "data": [
                    {"symbol": "AAPL", "report_date": "2026-06-27", "roa": 27.33},
                    {"symbol": "AAPL", "report_date": "2026-03-31", "roa": 26.10},
                    {"symbol": "NVDA", "report_date": "2026-07-28", "roa": 50.12},
                    {"symbol": "NVDA", "report_date": "2026-04-30", "roa": 48.90},
                ],
            },
        }

    monkeypatch.setattr(
        "dojo.datasource.huggingface.HuggingFaceAttributionFactorDataSource.fetch",
        mock_super_fetch,
    )

    res = ds.fetch(
        method="GET",
        path="/api/qdata/v1/stock/fin_indicators",
        params={"symbol": ["AAPL", "NVDA"], "limit": 1},
    )

    assert res["code"] == 0
    data = res["data"]
    assert data["total_num"] == 2
    assert isinstance(data["data"], dict)
    assert "AAPL" in data["data"]
    assert "NVDA" in data["data"]
    # Verify limit of 1 per symbol
    assert len(data["data"]["AAPL"]) == 1
    assert len(data["data"]["NVDA"]) == 1
    # Verify symbol column was popped from row records
    assert "symbol" not in data["data"]["AAPL"][0]
    assert data["data"]["AAPL"][0]["report_date"] == "2026-06-27"
    assert data["data"]["NVDA"][0]["report_date"] == "2026-07-28"


def test_offline_benchmark_kline_multi_symbol(monkeypatch) -> None:
    ds = HuggingFaceKlineDataSource()

    # Create dummy dataframe mimicking benchmark kline parquet
    df = pd.DataFrame(
        [
            {
                "symbol": "000001.SS",
                "bar_time": "2026-09-17 00:00:00",
                "open": 3877.0,
                "close": 3896.65,
                "kline_t": "1D",
            },
            {
                "symbol": "000001.SS",
                "bar_time": "2026-09-16 00:00:00",
                "open": 3860.0,
                "close": 3870.0,
                "kline_t": "1D",
            },
            {
                "symbol": "^SPX",
                "bar_time": "2026-09-17 00:00:00",
                "open": 5600.0,
                "close": 5620.0,
                "kline_t": "1D",
            },
            {
                "symbol": "^SPX",
                "bar_time": "2026-09-16 00:00:00",
                "open": 5580.0,
                "close": 5595.0,
                "kline_t": "1D",
            },
        ]
    )
    df["index_symbol"] = df.symbol
    df = df.set_index("index_symbol")

    monkeypatch.setattr(ds, "fetch_df", lambda path: df)

    # Test multi-symbol fetch with limit=1
    res = ds.fetch(
        method="GET",
        path="/api/qdata/v1/benchmark/kline",
        params={"symbol": "000001.SS,^SPX", "kline_t": "1D", "limit": 1},
    )

    assert res["code"] == 0
    data = res["data"]
    assert data["total_num"] == 2
    assert isinstance(data["data"], dict)
    assert "000001.SS" in data["data"]
    assert "^SPX" in data["data"]
    assert len(data["data"]["000001.SS"]) == 1
    assert len(data["data"]["^SPX"]) == 1
    assert data["data"]["000001.SS"][0]["open"] == 3877.0
    assert data["data"]["^SPX"][0]["open"] == 5600.0
