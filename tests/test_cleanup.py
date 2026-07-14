from dojo.datasource.huggingface import HuggingFaceDataSource
import os

os.environ["DOJO_LOG_LEVEL"] = "INFO"
ds = HuggingFaceDataSource()
result = ds.cleanup_cache()
print("Cleanup Result:", result)
