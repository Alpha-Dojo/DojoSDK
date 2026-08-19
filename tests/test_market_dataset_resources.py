from __future__ import annotations

import json
from pathlib import Path

import httpx
import pyarrow as pa
import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo
from dojo.datasource.huggingface import HuggingFaceDataSource
from dojo.datasource.registry import HFEndpointSpec

TARGETS = (
    (
        "get_constituents",
        "/api/qdata/v1/market/sectors/constituents",
        {"market": "cn", "limit": 20, "offset": 5},
    ),
    (
        "get_daily",
        "/api/qdata/v1/market/sectors/daily",
        {"market": "cn", "limit": 20, "offset": 5},
    ),
    (
        "get_ticker_daily",
        "/api/qdata/v1/market/tickers/daily",
        {"market": "cn", "limit": 20, "offset": 5},
    ),
    (
        "get_fundamentals_periods",
        "/api/qdata/v1/market/sectors/fundamentals/periods",
        {"market": "cn", "limit": 20},
    ),
    (
        "get_horizon_metrics_daily",
        "/api/qdata/v1/market/sectors/horizon-metrics/daily",
        {"market": "cn", "limit": 20, "offset": 5},
    ),
    (
        "get_theme_state_daily",
        "/api/qdata/v1/market/sectors/theme-state/daily",
        {"market": "cn", "limit": 20, "offset": 5},
    ),
)

WRITE_TARGETS = (
    ("create_constituents", "/api/qdata/v1/market/sectors/constituents"),
    ("create_daily", "/api/qdata/v1/market/sectors/daily"),
    ("create_ticker_daily", "/api/qdata/v1/market/tickers/daily"),
)

OPENAPI_TARGET_PATHS = {path for _method, path, _kwargs in TARGETS} | {
    "/api/qdata/v1/sector/movers",
    "/api/qdata/v1/market/sectors/factors/daily",
    "/api/qdata/v1/market/tickers/factors/daily",
    "/api/qdata/v1/market/benchmarks/daily",
    "/api/qdata/v1/benchmark",
}


def test_target_paths_are_frozen_in_openapi_snapshot() -> None:
    openapi_path = Path(__file__).parents[1] / "docs" / "qdata_openapi.json"
    paths = json.loads(openapi_path.read_text(encoding="utf-8"))["paths"]
    assert not (OPENAPI_TARGET_PATHS - paths.keys())
    assert all("get" in paths[path] for path in OPENAPI_TARGET_PATHS)


@pytest.mark.parametrize(
    ("method", "legacy_path"),
    (
        ("get_constituents", "/api/qdata/v1/sector/precomputed/constituents"),
        ("get_daily", "/api/qdata/v1/sector/precomputed/sector_daily"),
        ("get_ticker_daily", "/api/qdata/v1/sector/precomputed/ticker_daily"),
    ),
)
def test_offline_canonical_methods_use_registered_legacy_paths(monkeypatch, method: str, legacy_path: str) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "false")
    seen = []

    class FakeDataSource:
        def fetch(self, **request):
            seen.append(request)
            return {"code": 0, "data": {"total_num": 0, "data": []}}

    http_client = httpx.Client(transport=httpx.MockTransport(lambda _request: None))
    client = Dojo(http_client=http_client)
    client._data_source = FakeDataSource()
    try:
        getattr(client.sectors, method)(market="cn", limit=10, offset=2)
    finally:
        http_client.close()
    assert seen[0]["path"] == legacy_path
    assert seen[0]["params"]["offset"] == 2


def test_offline_filters_then_sorts_then_offsets_then_limits() -> None:
    table = pa.table(
        {
            "market": ["cn", "cn", "cn", "us"],
            "trade_date": ["2026-08-10", "2026-08-12", "2026-08-11", "2026-08-12"],
            "ticker": ["A", "B", "C", "D"],
        }
    )
    spec = HFEndpointSpec(
        repo_id="test/dataset",
        time_field="trade_date",
        start_param="start_date",
        end_param="end_date",
    )
    rows = HuggingFaceDataSource()._apply_filters(
        table,
        spec,
        {
            "market": "cn",
            "start_date": "2026-08-10",
            "end_date": "2026-08-12",
            "offset": 1,
            "limit": 1,
        },
    )
    assert [row["ticker"] for row in rows] == ["C"]


@pytest.mark.parametrize(("method", "path", "kwargs"), TARGETS)
def test_sync_market_dataset_paths(monkeypatch, method: str, path: str, kwargs: dict) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {"total": 1}, "data": [{"market": "cn"}]})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        result = getattr(client.sectors, method)(**kwargs)
    finally:
        http_client.close()
    assert result["meta"]["total"] == 1
    assert seen[0].url.path == path
    assert seen[0].url.params["market"] == "cn"


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path", "kwargs"), TARGETS)
async def test_async_market_dataset_paths(monkeypatch, method: str, path: str, kwargs: dict) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {}, "data": []})

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", http_client=http_client)
    try:
        await getattr(client.sectors, method)(**kwargs)
    finally:
        await http_client.aclose()
    assert seen[0].url.path == path


@pytest.mark.asyncio
@pytest.mark.parametrize(("method", "path"), WRITE_TARGETS)
@pytest.mark.parametrize(("replace", "http_method"), ((False, "POST"), (True, "PUT")))
async def test_async_market_dataset_writes(monkeypatch, method: str, path: str, replace: bool, http_method: str) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    async def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {}, "data": {"inserted": 1}})

    http_client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    client = AsyncDojo(api_key="test", http_client=http_client)
    try:
        result = await getattr(client.sectors, method)(observations=[{"market": "cn"}], replace=replace)
    finally:
        await http_client.aclose()
    assert result["data"] == {"inserted": 1}
    assert seen[0].method == http_method
    assert seen[0].url.path == path
    assert json.loads(seen[0].content) == {"observations": [{"market": "cn"}]}


@pytest.mark.parametrize(("method", "path"), WRITE_TARGETS)
def test_sync_market_dataset_writes(monkeypatch, method: str, path: str) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {}, "data": {"inserted": 1}})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        result = getattr(client.sectors, method)(observations=[{"market": "cn"}])
    finally:
        http_client.close()
    assert result["data"] == {"inserted": 1}
    assert seen[0].method == "POST"
    assert seen[0].url.path == path


def test_sector_movers_path_and_contract(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"markets": {"cn": {"as_of": "2026-08-12", "items": []}}})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        result = client.sectors.get_movers(market="cn", scope="L3", start_date="2026-08-01", end_date="2026-08-12")
    finally:
        http_client.close()
    assert result["markets"]["cn"]["items"] == []
    assert seen[0].url.path == "/api/qdata/v1/sector/movers"
    assert seen[0].url.params["start_date"] == "2026-08-01"
    assert seen[0].url.params["end_date"] == "2026-08-12"


def test_sector_movers_rejects_missing_date_range_before_request(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    http_client = httpx.Client(transport=httpx.MockTransport(lambda _request: pytest.fail("request must not be sent")))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        with pytest.raises(ValueError, match="start_date and end_date are required"):
            client.sectors.get_movers(start_date=None, end_date=None)
    finally:
        http_client.close()


def test_sector_movers_typed_response(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            200,
            json={
                "markets": {
                    "cn": {
                        "as_of": "2026-08-12",
                        "items": [
                            {
                                "rank": 1,
                                "sector": {"name": "Semiconductors"},
                                "level1_id": 1,
                                "level2_id": 2,
                                "level3_id": 7,
                                "change_percent": 1.25,
                                "absolute_change_percent": 1.25,
                                "total_market_cap": 1000000,
                                "effective_member_count": 8,
                            }
                        ],
                    }
                }
            },
        )

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", return_raw_data=False, http_client=http_client)
    try:
        result = client.sectors.get_movers(market="cn", start_date="2026-08-12", end_date="2026-08-12")
    finally:
        http_client.close()
    assert result.markets["cn"].items[0].level3_id == 7


def test_typed_dataset_response_preserves_data_and_meta(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")

    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"meta": {"total": 1}, "data": [{"ticker": "AAPL"}]})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(
        api_key="test",
        return_raw_data=False,
        http_client=http_client,
    )
    try:
        result = client.sectors.get_ticker_daily(market="us", ticker="AAPL")
    finally:
        http_client.close()
    assert result.meta == {"total": 1}
    assert result.data == [{"ticker": "AAPL"}]


@pytest.mark.parametrize(
    ("resource", "method", "kwargs", "path"),
    (
        (
            "sectors",
            "get_sector_factors_daily",
            {"market": "cn", "level3_id": 123},
            "/api/qdata/v1/market/sectors/factors/daily",
        ),
        (
            "sectors",
            "get_ticker_factors_daily",
            {"market": "us", "ticker": "AAPL"},
            "/api/qdata/v1/market/tickers/factors/daily",
        ),
        (
            "benchmark",
            "get_market_daily",
            {"market": "us"},
            "/api/qdata/v1/market/benchmarks/daily",
        ),
        ("benchmark", "get_info", {"tickers": "SPX"}, "/api/qdata/v1/benchmark"),
    ),
)
def test_remaining_online_dataset_paths(monkeypatch, resource: str, method: str, kwargs: dict, path: str) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {}, "data": []})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        getattr(getattr(client, resource), method)(**kwargs)
    finally:
        http_client.close()
    assert seen[0].url.path == path


def test_legacy_factor_alias_maps_date_and_rule(monkeypatch) -> None:
    monkeypatch.setenv("DOJO_ONLINE", "true")
    seen = []

    def handler(request: httpx.Request) -> httpx.Response:
        seen.append(request)
        return httpx.Response(200, json={"meta": {}, "data": []})

    http_client = httpx.Client(transport=httpx.MockTransport(handler))
    client = Dojo(api_key="test", http_client=http_client)
    try:
        client.sectors.get_precomputed_sector_alpha_factors_daily(
            market="cn",
            level3_id=123,
            trade_date="2026-08-12",
            factor_rule="alpha",
        )
    finally:
        http_client.close()
    assert seen[0].url.params["start_date"] == "2026-08-12"
    assert seen[0].url.params["end_date"] == "2026-08-12"
    assert seen[0].url.params["rule"] == "alpha"
