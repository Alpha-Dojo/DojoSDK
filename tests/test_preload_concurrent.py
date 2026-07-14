from dojo.datasource.huggingface import HuggingFaceKlineDataSource
import os

os.environ["DOJO_LOG_LEVEL"] = "INFO"

paths_to_preload = ["/api/qdata/v1/stock/kline", "/api/qdata/v1/forex/kline", "/api/qdata/v1/stock/info", "/api/qdata/v1/stock/news", "/api/qdata/v1/benchmark/kline"]

ds = HuggingFaceKlineDataSource()
ds.preload(paths_to_preload)
print("Concurrent preload completed successfully!")
