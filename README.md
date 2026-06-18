# DojoSDK

Official Python client SDK for the Dojo API.

## Installation

```bash
pip install dojosdk-0.1.0-py3-none-any.whl
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
