import pytest
import dojo
from dojo._exceptions import APIStatusError


async def run_safe(coro):
    try:
        await coro
    except APIStatusError as e:
        # Accept status errors (400, 404, 422, etc.) as the request successfully reached the server
        print(f"Server returned status {e.status_code}: {str(e)}")


@pytest.fixture
def client():
    # Construct AsyncDojo client. It loads API key and base URL from env variables (sourced from .env)
    return dojo.AsyncDojo()


@pytest.mark.asyncio
async def test_stocks(client):
    # Existing endpoints with examples from docs
    await run_safe(client.stocks.get_competitors(symbol="AAPL"))
    await run_safe(client.stocks.get_risk_metrics(symbol="AAPL"))
    await run_safe(client.stocks.get_market_history(symbol="AAPL"))
    await run_safe(client.stocks.get_quote(symbols=["AAPL", "601318.SS", "0700.HK"]))
    await run_safe(client.stocks.post_quote(body={"symbols": "AAPL,601318.SS,0700.HK"}))
    await run_safe(client.stocks.get_financials(symbol="AAPL"))
    await run_safe(client.stocks.get_history_quote(symbol="AAPL", limit=10))
    await run_safe(client.stocks.get_info(symbol="AAPL"))
    await run_safe(client.stocks.get_news(symbol="AAPL"))
    await run_safe(client.stocks.get_sentiments(symbol="AAPL"))

    # New /api/qdata/v1/stock/ endpoints with examples from docs
    await run_safe(client.stocks.get_ystock_info(market="cn", sector="Energy", only_simple_fields=True))
    await run_safe(client.stocks.get_kline(symbol="0700.HK", kline_t="1D", price_adj_type="pre", limit=100))
    await run_safe(client.stocks.get_kline_cs(market="hk", kline_t="1D", window_limit=10))
    await run_safe(client.stocks.get_market_summary())
    await run_safe(client.stocks.get_sector_industry_summary())
    await run_safe(client.stocks.get_kline_interval_stat(market="hk", kline_t="1D", window_limit=5))
    await run_safe(client.stocks.get_kline_interval_stat(symbols="AAPL,601318.SS,0700.HK", kline_t="1D", window_limit=22))
    await run_safe(client.stocks.get_stocks_market_summary(symbol="AAPL", limit=10))
    await run_safe(client.stocks.get_event_remind(symbol="AAPL"))
    await run_safe(client.stocks.get_fin_indicators(symbol="AAPL"))
    await run_safe(client.stocks.get_main_income(symbol="AAPL"))


@pytest.mark.asyncio
async def test_forex(client):
    await run_safe(client.forex.get_symbol_list())
    await run_safe(client.forex.get_current_quote(symbols="EURUSD,USDJPY"))
    await run_safe(client.forex.post_current_quote(body={"symbols": "EURUSD,USDJPY"}))
    await run_safe(client.forex.get_kline(symbol="EURUSD", kline_t="1d", limit=10))


@pytest.mark.asyncio
async def test_market_data(client):
    await run_safe(client.market_data.get_basic_info(exchange="binance", bz_type="spot"))
    await run_safe(client.market_data.get_ticker(exchange="binance", bz_type="spot", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_depth(exchange="binance", bz_type="spot", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_kline(exchange="binance", bz_type="spot", symbol="BTC-USDT", kline_t="1m"))
    await run_safe(client.market_data.get_mark_price(exchange="binance", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_funding_rate(exchange="binance", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_top_longshort(exchange="binance", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_volatility(exchange="binance", bz_type="spot", symbol="BTC-USDT"))
    await run_safe(client.market_data.get_indicator(exchange="binance", bz_type="spot", symbol="BTC-USDT", indicator="ma"))


@pytest.mark.asyncio
async def test_macro(client):
    await run_safe(client.macro.news.get(sector="Tech"))
    await run_safe(client.macro.metrics.get(indicator_key="GDP"))
    await run_safe(client.macro.sentiments.get(lookback=30))


@pytest.mark.asyncio
async def test_benchmark(client):
    await run_safe(client.benchmark.get_kline(symbol="SPY"))
    await run_safe(client.benchmark.get_price(symbols=["SPY"]))
    await run_safe(client.benchmark.get_performance(symbol="SPY"))


@pytest.mark.asyncio
async def test_concepts(client):
    await run_safe(client.concepts.get_info())
    await run_safe(client.concepts.get_constituents(concept_id="1"))
    await run_safe(client.concepts.get_quote(return_tickers=True))


@pytest.mark.asyncio
async def test_news(client):
    await run_safe(client.news.get_news())
    await run_safe(client.news.get_sentiment_score())
    await run_safe(client.news.get_titles())
    await run_safe(client.news.get_events())
    await run_safe(client.news.get_external_events())
    await run_safe(client.news.get_related_nodes(source_type="trading_economics", uq_id="123"))


@pytest.mark.asyncio
async def test_user(client):
    await run_safe(client.user.traits.get(user_id="test_user"))
    await run_safe(client.user.traits.update(body={"traits": {}}))
    await run_safe(client.user.traits.get_by_id(user_id="test_user"))
    await run_safe(client.user.traits.update_by_id(user_id="test_user", body={"traits": {}}))
    await run_safe(client.user.analytics.upload(body={"event": "test"}))


@pytest.mark.asyncio
async def test_sectors(client):
    await run_safe(client.sectors.get())
    await run_safe(client.sectors.get_metrics(metric_type="return"))
    await run_safe(client.sectors.get_info())
    await run_safe(client.sectors.create_info(body={"items": []}))
    await run_safe(client.sectors.get_symbol_relations())
    await run_safe(client.sectors.create_symbol_relations(body={"items": []}))


@pytest.mark.asyncio
async def test_strategy(client):
    await run_safe(client.strategy.get_demo())
    await run_safe(client.strategy.get_performance(strategy_id="1"))


@pytest.mark.asyncio
async def test_cache(client):
    await run_safe(client.cache.clear())


@pytest.mark.asyncio
async def test_indices(client):
    await run_safe(client.indices.get())


@pytest.mark.asyncio
async def test_instruments(client):
    await run_safe(client.instruments.get())
