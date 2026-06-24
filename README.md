# DojoSDK

Official Python client SDK for the Dojo API.

## Installation

```bash
pip install dojosdk
```

## Quick Start

```python
import dojo

client = dojo.Dojo(api_key="your-api-key")
ticker = client.market_data.get_ticker(exchange="BINANCE", bz_type="spot", symbol="BTCUSDT")
print(ticker)
```

## Environment Variables

When integrating DojoSDK with Hugging Face Datasets (e.g., for automated data syncing or pushing records), you need to configure the following environment variable to authenticate with Hugging Face:

| Environment Variable | Description | Required |
| --- | --- | --- |
| `HF_TOKEN` | Hugging Face User Access Token. Requires "Write" permissions to push data to remote repositories. | **Yes** (when using `huggingface_hub` to push without CLI login) |

**Setup Example:**
```bash
export HF_TOKEN="hf_your_access_token_here"
```
Alternatively, you can skip configuring this variable if your environment is already authenticated locally via `huggingface-cli login`.

## Hugging Face Cache Management

DojoSDK automatically caches offline data downloaded from Hugging Face. To free up disk space by deleting older revisions and keeping only the latest version of the cached data, use the `cleanup_cache` method:

```python
from dojo.datasource.huggingface import HuggingFaceDataSource

ds = HuggingFaceDataSource()
result = ds.cleanup_cache()

# Expected output format:
# {'freed_space': '3.0GB', 'details': {'AlphaDojo/dojo_stock_kline': '772.9M', ...}, 'message': 'Cache cleanup complete.'}
print(result)
```
