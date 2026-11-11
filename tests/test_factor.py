from __future__ import annotations

import datetime
import json

import httpx
import pytest
from pydantic import ValidationError

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo
from dojo.types import (
    FactorQueryRequest,
    FactorQueryResponse,
    FactorTableColumnInfo,
    FactorTableInfo,
    FactorTablesResponse,
    OrderBySpec,
)


def _query_response() -> dict:
    return {
        "message": "",
        "code": 0,
        "data": {
            "meta": {
                "table_name": "etf_daily_factors",
                "page": 1,
                "size": 100,
                "total_num": 1,
                "total_page": 1,
            },
            "data": [
                {
                    "as_of_date": "2026-10-01",
                    "ticker": "SPY",
                    "listing_market": "US",
                    "mom_20d": 0.042,
                }
            ],
        },
    }


def _tables_response() -> dict:
    return {
        "message": "",
        "code": 0,
        "data": {
            "total_num": 1,
            "data": [
                {
                    "table_name": "etf_daily_factors",
                    "namespace": "factor_store",
                    "description": "Daily ETF factors",
                    "time_column": "as_of_date",
                    "time_column_type": "DATE",
                    "symbol_column": "ticker",
                    "market_column": "listing_market",
                    "partition_columns": ["as_of_date"],
                    "key_columns": ["as_of_date", "ticker"],
                    "default_order_by": ["as_of_date desc", "ticker asc"],
                    "max_date_span_days": 366,
                    "max_date_span_days_with_symbols": 3650,
                    "columns": [
                        {"name": "as_of_date", "type": "DATE"},
                        {"name": "ticker", "type": "VARCHAR"},
                        {"name": "mom_20d", "type": "DOUBLE"},
                    ],
                }
            ],
        },
    }


def test_sync_factor_query_with_kwargs(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_query_response())

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        response = client.factor.query(
            table_name="etf_daily_factors",
            start_date=datetime.date(2026, 9, 1),
            end_date="2026-10-01",
            tickers=["SPY", "QQQ"],
            listing_market="US",
            filters={"mom_20d": {"gt": 0.0}},
            fields=["as_of_date", "ticker", "mom_20d"],
            order_by=[OrderBySpec(field="as_of_date", direction="desc"), "ticker asc"],
            page=2,
            size=50,
            include_total=True,
        )
    finally:
        http_client.close()

    assert len(seen) == 1
    assert seen[0].method == "POST"
    assert seen[0].url.path == "/api/qdata/v1/factor/query"
    sent_json = json.loads(seen[0].content)
    assert sent_json == {
        "table_name": "etf_daily_factors",
        "start_date": "2026-09-01",
        "end_date": "2026-10-01",
        "tickers": ["SPY", "QQQ"],
        "listing_market": "US",
        "filters": {"mom_20d": {"gt": 0.0}},
        "fields": ["as_of_date", "ticker", "mom_20d"],
        "order_by": [{"field": "as_of_date", "direction": "desc"}, "ticker asc"],
        "page": 2,
        "size": 50,
        "include_total": True,
    }
    assert response == _query_response()["data"]


def test_sync_factor_query_defaults_and_body_override(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_query_response())

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client, return_raw_data=False)
    try:
        # 1. Default call with no arguments
        res1 = client.factor.query()
        # 2. Call with FactorQueryRequest body + keyword override
        req_model = FactorQueryRequest(table_name="custom_factors", tickers="AAPL,MSFT", page=1)
        res2 = client.factor.query(body=req_model, page=3)
    finally:
        http_client.close()

    assert isinstance(res1, FactorQueryResponse)
    assert res1.meta["table_name"] == "etf_daily_factors"
    assert len(res1.data) == 1
    assert isinstance(res2, FactorQueryResponse)

    sent_1 = json.loads(seen[0].content)
    assert sent_1 == {
        "table_name": "etf_daily_factors",
        "page": 1,
        "size": 100,
        "include_total": False,
    }

    sent_2 = json.loads(seen[1].content)
    assert sent_2 == {
        "table_name": "custom_factors",
        "tickers": "AAPL,MSFT",
        "page": 3,
        "size": 100,
        "include_total": False,
    }


@pytest.mark.asyncio
async def test_async_factor_query(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_query_response())

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", http_client=http_client)
    try:
        response = await client.factor.query(
            body={"table_name": "etf_daily_factors", "listing_market": ["US", "HK"]},
            size=20,
        )
    finally:
        await http_client.aclose()

    assert len(seen) == 1
    assert seen[0].method == "POST"
    assert seen[0].url.path == "/api/qdata/v1/factor/query"
    sent_json = json.loads(seen[0].content)
    assert sent_json == {
        "table_name": "etf_daily_factors",
        "listing_market": ["US", "HK"],
        "page": 1,
        "size": 20,
        "include_total": False,
    }
    assert response == _query_response()["data"]


def test_sync_factor_get_tables_and_alias(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_tables_response())

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client, return_raw_data=False)
    try:
        res1 = client.factor.get_tables(
            table_name="etf_daily_factors",
            include_columns=False,
            refresh_schema=True,
        )
        res2 = client.factor.tables()
    finally:
        http_client.close()

    assert seen[0].method == "GET"
    assert seen[0].url.path == "/api/qdata/v1/factor/tables"
    assert dict(seen[0].url.params) == {
        "table_name": "etf_daily_factors",
        "include_columns": "false",
        "refresh_schema": "true",
    }
    assert dict(seen[1].url.params) == {}

    assert isinstance(res1, FactorTablesResponse)
    assert res1.total_num == 1
    assert isinstance(res1.data[0], FactorTableInfo)
    assert res1.data[0].table_name == "etf_daily_factors"
    assert isinstance(res1.data[0].columns[0], FactorTableColumnInfo)
    assert res2.total_num == 1


@pytest.mark.asyncio
async def test_async_factor_get_tables_and_alias(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_tables_response())

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", http_client=http_client)
    try:
        res1 = await client.factor.get_tables(table_name="etf_daily_factors")
        res2 = await client.factor.tables(include_columns=True, refresh_schema=False)
    finally:
        await http_client.aclose()

    assert seen[0].url.path == "/api/qdata/v1/factor/tables"
    assert dict(seen[0].url.params) == {"table_name": "etf_daily_factors"}
    assert dict(seen[1].url.params) == {"include_columns": "true", "refresh_schema": "false"}
    assert res1 == _tables_response()["data"]
    assert res2 == _tables_response()["data"]


def test_factor_query_validation_rejects_invalid_pagination(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(lambda req: httpx.Response(200, json=_query_response())))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        with pytest.raises(ValidationError):
            client.factor.query(page=0)
        with pytest.raises(ValidationError):
            client.factor.query(size=1001)
        with pytest.raises(ValidationError):
            client.factor.query(table_name="")
    finally:
        http_client.close()


def test_factor_query_order_by_dict_and_spec_serialization(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json=_query_response())

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        client.factor.query(
            order_by=[{"field": "as_of_date", "direction": "DESC"}, OrderBySpec(field="ticker")],
        )
        client.factor.query(order_by="as_of_date desc")
    finally:
        http_client.close()

    sent_1 = json.loads(seen[0].content)
    assert sent_1["order_by"] == [
        {"field": "as_of_date", "direction": "DESC"},
        {"field": "ticker", "direction": "asc"},
    ]
    sent_2 = json.loads(seen[1].content)
    assert sent_2["order_by"] == "as_of_date desc"
