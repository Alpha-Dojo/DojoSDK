from __future__ import annotations

from typing import Any, List, Dict
from pydantic import BaseModel, ConfigDict
from dojo._compat import PYDANTIC_V1


class DojoModel(BaseModel):

    if not PYDANTIC_V1:
        model_config = ConfigDict(extra="allow")
    else:

        class Config:
            extra = "allow"


# --- Stocks ---
class CompetitorsResponse(DojoModel):
    symbol: str
    competitors: List[str]


class RiskMetricsResponse(DojoModel):
    symbol: str
    beta: float | None = None
    var: float | None = None
    sharpe: float | None = None
    metrics: Dict[str, Any] | None = None


class MarketHistoryResponse(DojoModel):
    symbol: str
    history: List[Dict[str, Any]]


class CurrentQuoteResponse(DojoModel):
    symbol: str
    price: float
    volume: float | None = None
    high: float | None = None
    low: float | None = None
    timestamp: int | None = None
    quotes: List[Dict[str, Any]] | None = None


class FinancialsResponse(DojoModel):
    symbol: str
    financials: List[Dict[str, Any]]


class StockInfoResponse(DojoModel):
    symbol: str
    name: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    info: Dict[str, Any] | None = None


class StockNewsResponse(DojoModel):
    symbol: str
    news: List[Dict[str, Any]]


class StockSentimentResponse(DojoModel):
    symbol: str
    sentiment_score: float | None = None
    sentiments: List[Dict[str, Any]] | None = None


# --- Market Data ---
class BasicInfoResponse(DojoModel):
    exchange: str
    bz_type: str
    symbols: List[Dict[str, Any]]


class TickerResponse(DojoModel):
    exchange: str
    bz_type: str
    symbol: str | None = None
    price: float | None = None
    volume: float | None = None
    tickers: List[Dict[str, Any]] | None = None


class DepthResponse(DojoModel):
    exchange: str
    bz_type: str
    symbol: str | None = None
    bids: List[List[float]]
    asks: List[List[float]]
    timestamp: int | None = None


class KLineResponse(DojoModel):
    exchange: str
    bz_type: str
    symbol: str | None = None
    klines: List[List[Any]]


class MarkPriceResponse(DojoModel):
    exchange: str
    symbol: str | None = None
    mark_price: float
    funding_rate: float | None = None
    timestamp: int | None = None
    prices: List[Dict[str, Any]] | None = None


class FundingRateResponse(DojoModel):
    exchange: str
    symbol: str | None = None
    rates: List[Dict[str, Any]]


class TopLongShortResponse(DojoModel):
    exchange: str
    symbol: str | None = None
    long_short_ratio: float | None = None
    positions: List[Dict[str, Any]] | None = None


class VolatilityResponse(DojoModel):
    exchange: str
    symbol: str | None = None
    volatility: float | None = None
    history: List[Dict[str, Any]] | None = None


class IndicatorResponse(DojoModel):
    exchange: str
    symbol: str | None = None
    indicators: List[Dict[str, Any]]


class IndicesResponse(DojoModel):
    indices: List[Dict[str, Any]]


class InstrumentsResponse(DojoModel):
    instruments: List[Dict[str, Any]]


# --- Macro ---
class MacroNewsResponse(DojoModel):
    news: List[Dict[str, Any]]


class MacroMetricsResponse(DojoModel):
    metrics: List[Dict[str, Any]]


class MacroSentimentResponse(DojoModel):
    sentiments: List[Dict[str, Any]]


# --- Benchmark ---
class BenchmarkKLineResponse(DojoModel):
    symbol: str
    klines: List[List[Any]]


class BenchmarkPriceResponse(DojoModel):
    prices: List[Dict[str, Any]]


class BenchmarkPerformanceResponse(DojoModel):
    symbol: str
    performance: List[Dict[str, Any]]


class BenchmarkCatalogResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


# --- Concepts ---
class ConceptInfoResponse(DojoModel):
    concepts: List[Dict[str, Any]]


class ConceptConstituentsResponse(DojoModel):
    concept_id: str | None = None
    constituents: List[Dict[str, Any]]


class ConceptQuoteResponse(DojoModel):
    quotes: List[Dict[str, Any]]


# --- News ---
class NewsResponse(DojoModel):
    news: List[Dict[str, Any]]


class NewsScoreResponse(DojoModel):
    scores: List[Dict[str, Any]]


class NewsTitleResponse(DojoModel):
    titles: List[Dict[str, Any]]


class StockEventResponse(DojoModel):
    events: List[Dict[str, Any]]


class ExternalEventsResponse(DojoModel):
    events: List[Dict[str, Any]]


# --- User ---
class UserTraitsResponse(DojoModel):
    user_id: str | None = None
    traits: Dict[str, Any] | None = None
    success: bool | None = None


class UserAnalyticsResponse(DojoModel):
    success: bool
    message: str | None = None


# --- Sectors ---
class SectorsResponse(DojoModel):
    sectors: List[Dict[str, Any]]


class SectorMetricsResponse(DojoModel):
    metrics: List[Dict[str, Any]]


# --- Strategy ---
class StrategyDemoResponse(DojoModel):
    strategies: List[Dict[str, Any]]


class StrategyPerformanceResponse(DojoModel):
    strategy_id: str
    performance: List[Dict[str, Any]]


# --- Cache ---
class CacheResponse(DojoModel):
    success: bool
    message: str | None = None


# --- News (Added Endpoints) ---
class ExternalEventRelatedNodesResponse(DojoModel):
    event: Dict[str, Any]
    graph_root: Dict[str, Any]
    nodes: List[Dict[str, Any]] | None = None
    edges: List[Dict[str, Any]] | None = None
    meta: Dict[str, Any]


# --- Sector (Added Endpoints) ---
class SectorInfoListResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]] | None = None


class SectorInfoCreateRequest(DojoModel):
    items: List[Dict[str, Any]]


class SectorInfoCreateResponse(DojoModel):
    created: int


class SectorSymbolRelationListResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]] | None = None


class SectorSymbolRelationCreateRequest(DojoModel):
    items: List[Dict[str, Any]]


class SectorSymbolRelationCreateResponse(DojoModel):
    created: int


# --- Stocks (Added Endpoints) ---
class YStockInfoItem(DojoModel):
    ticker: str
    short_name: str | None = None
    long_name: str | None = None
    market: str | None = None
    full_exchange_name: str | None = None
    city: str | None = None
    zip: str | None = None
    country: str | None = None
    phone: str | None = None
    website: str | None = None
    fax: str | None = None
    industry: str | None = None
    sector: str | None = None


class YStockInfoResponse(DojoModel):
    total_num: int
    stocks: List[YStockInfoItem]


class StockKlineResponseItem(DojoModel):
    symbol: str
    kline_t: str
    bar_time: str
    open: float | None = None
    high: float | None = None
    low: float | None = None
    close: float | None = None
    vol: float | None = None
    amount: float | None = None
    change_p: float | None = None
    tr: float | None = None
    adj_factor_cum: float | None = 1.0
    dividends: float | None = None
    splits: float | None = None


class StockKlineResponse(DojoModel):
    total_num: int
    data: List[StockKlineResponseItem]


class StockKlineCSResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]]


class StockMarketSummaryResponse(DojoModel):
    total_num: int
    summary: Dict[str, Any]


class StockSectorIndustrySummaryResponse(DojoModel):
    total_num: int
    summary: Dict[str, Any]


class StockKlineIntervalStatResponse(DojoModel):
    total_num: int
    stats: List[Dict[str, Any]]


class StocksMarketSummaryItem(DojoModel):
    ticker: str
    summary: str


class StocksMarketSummaryResponse(DojoModel):
    total_num: int
    data: List[StocksMarketSummaryItem]


# --- Stocks (OpenAPI sync: event remind / financial indicators / main income) ---
class StockEventRemindResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class StockFinIndicatorsResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class StockMainIncomeResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


# --- Forex ---
class ForexCurrentQuoteResponse(DojoModel):
    quotes: List[Dict[str, Any]] | None = None


class ForexKlineResponse(DojoModel):
    symbol: str | None = None
    klines: List[List[Any]] | None = None


class ForexSymbolListResponse(DojoModel):
    symbols: List[Dict[str, Any]] | None = None


# --- Sector Precomputed ---
class SectorPrecomputedConstituentsResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedTickerDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedFundamentalsPeriodResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedMarketBenchmarkDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedSectorAlphaFactorsDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedTickerAlphaFactorsDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedSectorHorizonMetricsResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class SectorPrecomputedThemeStateDailyResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


# --- Analysis ---
class AnalysisMarketDynamicsResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class AnalysisTopicDiscoveriesResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class MarketDynamicsItem(DojoModel):
    event_time: str
    event_summary: Dict[str, Any]
    sector_impacts: List[Dict[str, Any]]


class MarketDynamicsCreateRequest(DojoModel):
    items: List[MarketDynamicsItem]


class MarketDynamicsCreateResponse(DojoModel):
    created: int
