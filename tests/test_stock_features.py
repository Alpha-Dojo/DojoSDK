from __future__ import annotations

import datetime
import os

import pytest

from dojo.client.async_client import AsyncDojo
from dojo.client.sync import Dojo

def _make_kwargs() -> dict:
    kwargs = {}
    if base_url := os.getenv("DOJO_BASE_URL"):
        kwargs["base_url"] = base_url
    return kwargs


# ------------------------------------------------ categories by parent (async)
@pytest.mark.asyncio
@pytest.mark.skipif(
    not os.getenv("DOJO_API_KEY"),
    reason="DOJO_API_KEY not set; skip real-environment test",
)
async def test_async_get_stock_features() -> None:
    """Real-environment test (no mock): list children of a top-level category."""
    api_key = os.environ["DOJO_API_KEY"]

    client = AsyncDojo(api_key=api_key, **_make_kwargs())
    try:
        response = await client.stocks.get_stock_features(symbol=["AAPL", "MSFT", "600519.SS"])
    finally:
        pass

    assert isinstance(response, dict)

    data = response["data"]
    assert isinstance(data, dict)
    assert response["total_num"] == len(data)
    print(data)
    for key,items in data.items():
        print(key,len(items))



# ------------------------------------------------ categories by parent (async)
@pytest.mark.skipif(
    not os.getenv("DOJO_API_KEY"),
    reason="DOJO_API_KEY not set; skip real-environment test",
)
def test_sync_get_stock_features() -> None:
    """Real-environment test (no mock): list children of a top-level category."""
    api_key = os.environ["DOJO_API_KEY"]

    client = Dojo(api_key=api_key, **_make_kwargs())
    try:
        response = client.stocks.get_stock_features(symbol=["AAPL", "MSFT", "600519.SS"]
                                                    ,start_trading_date=datetime.datetime(2025, 1, 1))
    finally:
        pass

    assert isinstance(response, dict)

    data = response["data"]
    assert isinstance(data, dict)
    assert response["total_num"] == len(data)
    for key,items in data.items():
        print(key,len(items))
