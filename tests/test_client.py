import pytest
import respx
import httpx
import dojo

# --- Setup Mocks and Fixtures ---


@pytest.fixture
def sync_client():
    return dojo.Dojo(api_key="test-api-key", base_url="https://api.flowhale.ai")


@pytest.fixture
def async_client():
    return dojo.AsyncDojo(api_key="test-api-key", base_url="https://api.flowhale.ai")


def test_missing_api_key():
    import os

    orig_env = os.environ.get("DOJO_API_KEY")
    if "DOJO_API_KEY" in os.environ:
        del os.environ["DOJO_API_KEY"]
    try:
        with pytest.raises(dojo.DojoError):
            dojo.Dojo()
    finally:
        if orig_env is not None:
            os.environ["DOJO_API_KEY"] = orig_env


@respx.mock
def test_sync_request_success(sync_client):
    respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL&limit=5").mock(
        return_value=httpx.Response(200, json={"symbol": "AAPL", "competitors": ["MSFT", "GOOGL"]})
    )
    resp = sync_client.stocks.get_competitors(symbol="AAPL", limit=5)
    assert resp.symbol == "AAPL"
    assert resp.competitors == ["MSFT", "GOOGL"]


@respx.mock
@pytest.mark.asyncio
async def test_async_request_success(async_client):
    respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL").mock(return_value=httpx.Response(200, json={"symbol": "AAPL", "competitors": ["MSFT"]}))
    resp = await async_client.stocks.get_competitors(symbol="AAPL")
    assert resp.symbol == "AAPL"
    assert resp.competitors == ["MSFT"]


@respx.mock
def test_retry_on_server_error(sync_client):
    # Mock first request failing with 500, second succeeding with 200
    route = respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL")
    route.side_effect = [httpx.Response(500), httpx.Response(200, json={"symbol": "AAPL", "competitors": []})]

    # We set default retries = 1, so the 1st request fails, retries once and succeeds.
    resp = sync_client.stocks.get_competitors(symbol="AAPL")
    assert resp.symbol == "AAPL"
    assert route.call_count == 2


@respx.mock
def test_no_retries_remaining_raises_error(sync_client):
    # Mock all requests failing with 500
    route = respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL")
    route.mock(return_value=httpx.Response(500, json={"detail": "Server error"}))

    # max_retries = 1, so it makes 1 attempt + 1 retry = 2 total requests before raising error
    with pytest.raises(dojo.InternalServerError) as exc_info:
        sync_client.stocks.get_competitors(symbol="AAPL")

    assert exc_info.value.status_code == 500
    assert route.call_count == 2


@respx.mock
def test_rate_limit_error(sync_client):
    respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL").mock(return_value=httpx.Response(429, json={"detail": "Too many requests"}))

    with pytest.raises(dojo.RateLimitError) as exc_info:
        sync_client.stocks.get_competitors(symbol="AAPL")

    assert exc_info.value.status_code == 429
    assert "Too many requests" in str(exc_info.value)


@respx.mock
def test_validation_error(sync_client):
    # Returning invalid response data (e.g. competitors field is missing/invalid type)
    respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL").mock(return_value=httpx.Response(200, json={"symbol": "AAPL", "competitors": None}))

    with pytest.raises(dojo.APIResponseValidationError) as exc_info:
        sync_client.stocks.get_competitors(symbol="AAPL")

    assert exc_info.value.status_code == 200
    assert exc_info.value.body == {"symbol": "AAPL", "competitors": None}


@respx.mock
def test_with_raw_response(sync_client):
    respx.get("https://api.flowhale.ai/api/qdata/v1/stocks/competitors?symbol=AAPL").mock(
        return_value=httpx.Response(200, json={"symbol": "AAPL", "competitors": ["MSFT"]}, headers={"X-Test-Header": "working"})
    )

    # Access raw response
    raw_resp = sync_client.stocks.with_raw_response.get_competitors(symbol="AAPL")

    assert isinstance(raw_resp, dojo.client.base.APIResponse)
    assert raw_resp.status_code == 200
    assert raw_resp.headers.get("X-Test-Header") == "working"
    assert raw_resp.parsed_data.symbol == "AAPL"
    assert raw_resp.parsed_data.competitors == ["MSFT"]
