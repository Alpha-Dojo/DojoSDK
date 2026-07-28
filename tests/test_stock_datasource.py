from unittest.mock import patch
import pyarrow as pa
from dojo.datasource.huggingface import StockDataSource, HuggingFaceDataSource


def test_stock_datasource_inheritance():
    assert issubclass(StockDataSource, HuggingFaceDataSource)


def test_stock_datasource_ystock_info_symbols_mapping():
    ds = StockDataSource()

    # Create a mock PyArrow table representing dojo_stock_info (with 'ticker' column)
    table = pa.Table.from_pydict(
        {
            "ticker": ["AAPL", "MSFT", "GOOGL"],
            "name": ["Apple Inc.", "Microsoft Corp.", "Alphabet Inc."],
        }
    )

    with patch.object(ds, "_load_dataset", return_value=table):
        # 1. Single symbol
        res = ds.fetch(method="GET", path="/api/qdata/v1/stock/ystock_info", params={"symbols": "AAPL"})
        assert res["code"] == 0
        data = res["data"]["data"]
        assert len(data) == 1
        assert data[0]["ticker"] == "AAPL"

        # 2. Comma separated symbols
        res2 = ds.fetch(method="GET", path="/api/qdata/v1/stock/ystock_info", params={"symbols": "AAPL,MSFT"})
        assert res2["code"] == 0
        data2 = res2["data"]["data"]
        assert len(data2) == 2
        tickers = [d["ticker"] for d in data2]
        assert "AAPL" in tickers and "MSFT" in tickers

        # 3. List of symbols in params
        res3 = ds.fetch(method="GET", path="/api/qdata/v1/stock/ystock_info", params={"symbols": ["GOOGL"]})
        assert res3["code"] == 0
        data3 = res3["data"]["data"]
        assert len(data3) == 1
        assert data3[0]["ticker"] == "GOOGL"
