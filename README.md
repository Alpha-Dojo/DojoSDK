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
