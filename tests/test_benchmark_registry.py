from dojo.datasource.registry import resolve


def test_benchmark_kline_endpoint_warms_catalog_companion_file() -> None:
    spec = resolve("/api/qdata/v1/benchmark/kline")

    assert spec is not None
    assert spec.path_template == "data.parquet"
    assert spec.companion_files == ("benchmark.parquet",)


def test_benchmark_catalog_endpoint_reads_benchmark_parquet() -> None:
    spec = resolve("/api/qdata/v1/benchmark/catalog")

    assert spec is not None
    assert spec.path_template == "benchmark.parquet"
    assert spec.envelope == "list"
