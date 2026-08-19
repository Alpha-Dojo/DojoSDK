from unittest.mock import patch

import pandas as pd

from dojo.datasource.huggingface import HuggingFaceDataSource, HuggingFaceKlineDataSource, StockDataSource


def test_kline_fetch_filters_cached_dataframe_without_parent_fetch() -> None:
    df = pd.DataFrame(
        {
            "symbol": ["AAPL", "AAPL", "MSFT"],
            "kline_t": ["1D", "1H", "1D"],
            "bar_time": pd.to_datetime(["2024-01-01", "2024-01-02", "2024-01-01"]),
            "close": [10.0, float("nan"), 20.0],
        }
    )
    df["index_symbol"] = df["symbol"]
    df = df.set_index("index_symbol")
    cache_key = "AlphaDojo/dojo_stock_kline/data.parquet"
    source = HuggingFaceKlineDataSource()

    with (
        patch.object(source, "_df_cache", {cache_key: df}),
        patch.object(HuggingFaceDataSource, "fetch", side_effect=AssertionError("parent fetch used")),
    ):
        response = source.fetch(
            method="GET",
            path="/api/qdata/v1/stock/kline",
            params={"symbol": "AAPL,MSFT", "kline_t": "1D", "limit": 2},
        )

    assert response == {
        "code": 0,
        "message": "ok",
        "data": {
            "total_num": 2,
            "data": [
                {"symbol": "AAPL", "kline_t": "1D", "bar_time": "2024-01-01T00:00:00", "close": 10.0},
                {"symbol": "MSFT", "kline_t": "1D", "bar_time": "2024-01-01T00:00:00", "close": 20.0},
            ],
        },
    }

    with patch.object(source, "fetch_df", return_value=df):
        indexed = source.fetch(
            method="GET",
            path="/api/qdata/v1/stock/kline",
            params={"symbol": "AAPL", "kline_t": "1H", "index": 0},
        )

    assert indexed["data"]["data"] == [{"symbol": "AAPL", "kline_t": "1H", "bar_time": "2024-01-02T00:00:00", "close": None}]

    with patch.object(source, "fetch_df", return_value=df.reset_index(drop=True)):
        missing = source.fetch(
            method="GET",
            path="/api/qdata/v1/stock/kline",
            params={"symbol": "UNKNOWN"},
        )

    assert missing["data"] == {"total_num": 0, "data": []}

    with patch.object(StockDataSource, "fetch", return_value={"delegated": True}):
        delegated = source.fetch(
            method="GET",
            path="/api/qdata/v1/stock/ystock_info",
            params={},
        )

    assert delegated == {"delegated": True}
