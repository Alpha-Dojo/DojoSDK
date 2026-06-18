import pandas as pd
import pyarrow.parquet as pq
from dojo.utils.parquet_utils import pandas_to_parquet_with_metadata


def test_roundtrip():
    # 1. Create a dummy dataframe with an empty dict
    data = [{"symbol": "AAPL", "extra": {}, "normal_str": "{not json}", "my_list": [1, 2, 3]}, {"symbol": "MSFT", "extra": {"key": "value"}, "normal_str": "test2", "my_list": []}]
    df = pd.DataFrame(data)

    # 2. Serialize and write
    pandas_to_parquet_with_metadata(df, "test_metadata.parquet")

    # 3. Read back and check PyArrow table metadata
    table = pq.read_table("test_metadata.parquet")
    metadata = table.schema.metadata
    print("Metadata:", metadata)

    # 4. Simulate HuggingFaceDataSource behavior
    rows = table.to_pylist()
    print("Raw pylist rows:")
    print(rows)

    if metadata and b"dojosdk:json_columns" in metadata:
        import json

        json_cols = set(metadata[b"dojosdk:json_columns"].decode("utf-8").split(","))
        print(f"Detected JSON cols: {json_cols}")
        for row in rows:
            for col in json_cols:
                val = row.get(col)
                if isinstance(val, str):
                    try:
                        row[col] = json.loads(val)
                    except json.JSONDecodeError:
                        pass

    print("Deserialized rows:")
    print(rows)

    # Clean up
    import os

    os.remove("test_metadata.parquet")


if __name__ == "__main__":
    test_roundtrip()
