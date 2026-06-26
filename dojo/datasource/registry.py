from __future__ import annotations

from dataclasses import dataclass


@dataclass
class HFEndpointSpec:
    """Describes how a single API endpoint fetches data from a HuggingFace dataset."""

    repo_id: str
    repo_type: str = "dataset"

    # File path template rendered with request parameters
    path_template: str = "data.parquet"

    # Fallback template if specific dimension might be missing
    fallback_template: str | None = None

    # Additional files that should be warmed into cache for this endpoint.
    # These files may use a different schema and are not filtered as the main table.
    companion_files: tuple[str, ...] = ()

    # Filtering dimensions
    time_field: str | None = None
    start_param: str = "start_time"
    end_param: str = "end_time"
    symbol_field: str | None = None
    symbol_param: str = "symbol"

    limit_param: str = "limit"
    order_desc: bool = True

    # Projection (column pruning)
    fields_param: str | None = "include_fields"

    # JSON deserialization columns
    json_columns: list[str] | None = None

    # Envelope wrapping format: "list" or "dict"
    envelope: str = "list"


HF_REGISTRY: dict[str, HFEndpointSpec] = {
    "/api/qdata/v1/benchmark/kline": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_benchmark_kline",
        path_template="data.parquet",
        companion_files=("benchmark.parquet",),
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/benchmark/catalog": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_benchmark_kline",
        path_template="benchmark.parquet",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/sector/info": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_info",
        path_template="data.parquet",
        json_columns=["properties", "extra", "children"],
        envelope="list",
    ),
    "/api/qdata/v1/stock/ystock_info": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_stock_info",
        path_template="data.parquet",
        fallback_template="data.parquet",
        symbol_field="ticker",
        symbol_param="symbols",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/stocks/current_quote": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_quote",
        path_template="data.parquet",
        symbol_field="symbol",
        symbol_param="symbols",  # The parameter is usually 'symbols' which can be a list or comma separated string
        json_columns=["bid_prices"],
        envelope="list",
    ),
    "/api/qdata/v1/stock/kline": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_stock_kline",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/stock/fin_indicators": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_fin_indicators",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/stock/event_remind": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_event_remind",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/stock/main_income": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_main_income",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/forex/kline": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_forex_kline",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/sector/symbol_relations": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_symbol_relations",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=["primary", "secondary"],
        envelope="list",
    ),
    "/api/qdata/v1/stocks/news": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_stock_news",
        path_template="data.parquet",
        symbol_field="symbol",
        json_columns=["tickers", "keywords", "insights", "publisher"],
        envelope="list",
    ),
    "/api/qdata/v1/sector/precomputed/constituents": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_precomputed",
        path_template="constituents.parquet",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/sector/precomputed/sector_daily": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_precomputed",
        path_template="sector_daily.parquet",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/sector/precomputed/ticker_daily": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_precomputed",
        path_template="ticker_daily.parquet",
        json_columns=[],
        envelope="list",
    ),
    "/api/qdata/v1/sector/precomputed/manifest": HFEndpointSpec(
        repo_id="AlphaDojo/dojo_sector_precomputed",
        path_template="manifest.json",
        json_columns=[],
        envelope="dict",
    ),
    # Additional endpoints can be added here
}


def resolve(path: str) -> HFEndpointSpec | None:
    return HF_REGISTRY.get(path)
