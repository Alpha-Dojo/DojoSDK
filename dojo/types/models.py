from __future__ import annotations

from typing import Any, Dict, List, Literal
from pydantic import BaseModel, ConfigDict, Field
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
    total_num: int
    data: List[Dict[str, Any]]


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
    total_num: int
    data: List[Dict[str, Any]]


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
    total_num: int
    data: List[Dict[str, Any]]


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
    total_num: int
    data: List[Dict[str, Any]]


class BenchmarkPriceResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]]


class BenchmarkPerformanceResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]]


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
    data: List[YStockInfoItem]


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
    total_num: int
    data: List[Dict[str, Any]]


class ForexKlineResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]]


class ForexSymbolListResponse(DojoModel):
    total_num: int
    data: List[Dict[str, Any]]


# --- Market datasets / legacy sector precomputed compatibility ---
class DatasetResponse(DojoModel):
    data: List[Dict[str, Any]] | None = None
    meta: Dict[str, Any] | None = None
    total_num: int | None = None


class DatasetWriteRequest(DojoModel):
    observations: List[Dict[str, Any]] = Field(min_length=1, max_length=10000)


class DatasetWriteResponse(DojoModel):
    data: Dict[str, Any] | None = None
    meta: Dict[str, Any] | None = None


class SectorPrecomputedConstituentsResponse(DatasetResponse):
    pass


class SectorPrecomputedDailyResponse(DatasetResponse):
    pass


class SectorPrecomputedTickerDailyResponse(DatasetResponse):
    pass


class SectorPrecomputedFundamentalsPeriodResponse(DatasetResponse):
    pass


class SectorPrecomputedMarketBenchmarkDailyResponse(DatasetResponse):
    pass


class SectorPrecomputedSectorAlphaFactorsDailyResponse(DatasetResponse):
    pass


class SectorPrecomputedTickerAlphaFactorsDailyResponse(DatasetResponse):
    pass


class SectorPrecomputedSectorHorizonMetricsResponse(DatasetResponse):
    pass


class SectorPrecomputedThemeStateDailyResponse(DatasetResponse):
    pass


class SectorMoverItem(DojoModel):
    rank: int
    sector: Dict[str, Any]
    level1_id: int
    level2_id: int
    level3_id: int
    change_percent: float
    absolute_change_percent: float
    total_market_cap: float
    effective_member_count: int


class SectorMoversMarket(DojoModel):
    as_of: str | None = None
    items: List[SectorMoverItem] = Field(default_factory=list)


class SectorMoversResponse(DojoModel):
    markets: Dict[str, SectorMoversMarket] = Field(default_factory=dict)


# --- Analysis ---
class AnalysisMarketDynamicsResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class AnalysisTopicDiscoveriesResponse(DojoModel):
    total_num: int | None = None
    data: List[Dict[str, Any]] | None = None


class MarketDynamicsItem(DojoModel):
    market: Literal["us", "hk", "cn"]
    trading_date: str
    event_time: str
    event_summary: Dict[str, Any]
    sector_impacts: List[Dict[str, Any]]


class MarketDynamicsCreateRequest(DojoModel):
    items: List[MarketDynamicsItem]


class MarketDynamicsCreateResponse(DojoModel):
    data: List[Dict[str, Any]] = Field(default_factory=list)


class AttributionFactorItem(DojoModel):
    id: int | None = None
    factor_uid: str | None = None
    claim: Dict[str, Any] | None = None
    sector_id: int | str | None = None
    sector_ref: str | None = None
    market: str | None = None
    factor_topic: str | None = None
    role: str | None = None
    price_direction: str | None = None
    importance: str | None = None
    mechanism: Dict[str, Any] | None = None
    evidence: List[Dict[str, Any]] | None = None
    affected_tickers: List[str] | None = None
    event_time: str | None = None
    attrs: Dict[str, Any] | None = None


class AttributionFactorResponse(DojoModel):
    total_num: int | None = None
    data: List[AttributionFactorItem] | List[Dict[str, Any]] | None = None


class LocalizedText(DojoModel):
    zh: str
    en: str


class AttributionEvidence(DojoModel):
    quote: str = Field(min_length=1)
    url: str | None = None
    title: str | None = None


class AttributionFactorWriteItem(DojoModel):
    claim: LocalizedText
    sector_id: str = Field(min_length=1, max_length=128)
    market: Literal["us", "cn", "hk"]
    factor_topic: Literal[
        "earnings",
        "corporate_action",
        "policy_reg",
        "demand_supply",
        "product_tech",
        "capital_market",
        "market_structure",
        "analyst_revision",
        "exogenous_shock",
        "macro",
    ]
    factor_uid: str | None = Field(default=None, min_length=1, max_length=128)
    evidence: List[AttributionEvidence] | None = None
    affected_tickers: List[str] | None = None
    role: Literal["explains_move", "open_risk", "open_catalyst", "context"] = "explains_move"
    price_direction: Literal["up", "down", "mixed"] | None = None
    importance: Literal["high", "medium", "low"] | None = None
    mechanism: LocalizedText | None = None
    event_time: str | None = None
    payload_status: Literal["ready", "rejected"] = "ready"
    stance: Literal["positive", "negative", "neutral", "mixed"] | None = None
    attrs: Dict[str, Any] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class AttributionFactorWriteRequest(DojoModel):
    items: List[AttributionFactorWriteItem] = Field(min_length=1, max_length=10000)


class AttributionFactorWriteResult(DojoModel):
    id: int
    factor_uid: str
    market: str
    sector_id: int | None = None
    sector_ref: str | None = None
    factor_topic: str
    role: str
    payload_status: str
    price_direction: str | None = None
    importance: str | None = None
    stance: str | None = None
    claim: LocalizedText | None = None
    mechanism: LocalizedText | None = None
    event_time: str | None = None
    evidence: Any = None
    affected_tickers: List[str] | None = None
    attrs: Any = None


class AttributionFactorWriteResponse(DojoModel):
    data: List[AttributionFactorWriteResult] | None = None


class SectorBriefTitle(DojoModel):
    zh: str = Field(min_length=1, max_length=24)
    en: str = Field(min_length=1, max_length=60)


class SectorBriefDetail(DojoModel):
    zh: str = Field(min_length=1, max_length=80)
    en: str = Field(min_length=1, max_length=160)


class SectorBriefRoleLabel(DojoModel):
    zh: str = Field(min_length=1, max_length=8)
    en: str = Field(min_length=1, max_length=24)


class SectorBriefThesis(DojoModel):
    zh: str = Field(min_length=1, max_length=24)
    en: str = Field(min_length=1, max_length=60)


class SectorBriefDriver(DojoModel):
    title: SectorBriefTitle
    detail: SectorBriefDetail | None = None
    importance: Literal["high", "medium", "low"]
    price_direction: Literal["up", "down", "mixed"]


class SectorBriefRisk(DojoModel):
    title: SectorBriefTitle
    detail: SectorBriefDetail | None = None
    importance: Literal["high", "medium", "low"]


class SectorBriefComponent(DojoModel):
    ticker: str = Field(min_length=1, max_length=16, pattern=r"^[A-Za-z0-9.]+$")
    role_label: SectorBriefRoleLabel
    thesis: SectorBriefThesis


class SectorBriefExtractWriteItem(DojoModel):
    market: Literal["us", "cn", "hk"]
    sector_id: str = Field(min_length=1, max_length=128)
    as_of_date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    brief_uid: str | None = Field(default=None, min_length=1, max_length=128)
    key_drivers: List[SectorBriefDriver] = Field(max_length=5)
    key_risks: List[SectorBriefRisk] = Field(max_length=4)
    top_components: List[SectorBriefComponent] = Field(max_length=8)


class SectorBriefExtractItem(SectorBriefExtractWriteItem):
    id: int | None = None
    created_at: str | None = None
    updated_at: str | None = None


class SectorBriefExtractListResponse(DojoModel):
    total_num: int | None = None
    data: List[SectorBriefExtractItem] | List[Dict[str, Any]] | None = None


class SectorBriefExtractWriteRequest(DojoModel):
    items: List[SectorBriefExtractWriteItem] = Field(min_length=1, max_length=10000)


class SectorBriefExtractWriteResponse(DojoModel):
    data: List[SectorBriefExtractItem] | None = None
