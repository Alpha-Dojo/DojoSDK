import json
from typing import Any


def pandas_to_parquet_with_metadata(df: Any, path_or_buf: Any, **kwargs) -> None:
    """
    Serializes complex columns (dict, list) in a pandas DataFrame to JSON strings,
    injects a custom metadata key into the Parquet schema to indicate which columns were serialized,
    and writes the DataFrame to a Parquet file.

    Parameters
    ----------
    df : pandas.DataFrame
        The DataFrame to write.
    path_or_buf : str or file-like
        The path or buffer to write the Parquet file to.
    **kwargs
        Additional kwargs passed to pyarrow.parquet.write_table.
    """
    try:
        import pyarrow as pa
        import pyarrow.parquet as pq
        import pandas as pd
    except ImportError as e:
        raise ImportError(f"Missing required dependencies for parquet operations: {e}")

    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    json_columns = []

    # Identify and serialize complex columns
    for col in df.columns:
        # Check if any element in the column is a list or dict
        has_complex = df[col].apply(lambda x: isinstance(x, (dict, list))).any()
        if has_complex:
            json_columns.append(str(col))
            # Convert to JSON string
            df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, (dict, list)) else x)

    df = df.reset_index(drop=True)
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)

    # Extract existing metadata or create new dict
    metadata = table.schema.metadata or {}

    # Inject our custom metadata key if we serialized anything
    if json_columns:
        metadata[b"dojosdk:json_columns"] = ",".join(json_columns).encode("utf-8")
        table = table.replace_schema_metadata(metadata)

    # Write to Parquet
    pq.write_table(table, path_or_buf, **kwargs)
