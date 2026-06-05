from __future__ import annotations

from typing import Any, List
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    CompetitorsResponse,
    RiskMetricsResponse,
    MarketHistoryResponse,
    CurrentQuoteResponse,
    FinancialsResponse,
    StockInfoResponse,
    StockNewsResponse,
    StockSentimentResponse,
    YStockInfoResponse,
    StockKlineResponse,
    StockKlineCSResponse,
    StockMarketSummaryResponse,
    StockSectorIndustrySummaryResponse,
    StockKlineIntervalStatResponse,
    StocksMarketSummaryResponse,
)


class Stocks(SyncAPIResource):

    def get_competitors(self, *, symbol: str, limit: int | None = None) -> CompetitorsResponse:
        """Retrieves a list of competitor symbols for a stock.

        Parameters
        ----------
        symbol : str
            The ticker symbol of the target stock (e.g. AAPL).
        limit : int, optional
            Maximum number of competitors to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/stocks/competitors", cast_to=CompetitorsResponse, options={"params": params})

    def get_risk_metrics(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        lookback: int | None = None,
        benchmark_ticker: str | None = None,
    ) -> RiskMetricsResponse:
        """Retrieves risk metrics (such as beta, value-at-risk) for a stock.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        lookback : int, optional
            Lookback period length.
        benchmark_ticker : str, optional
            Ticker to calculate beta against.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if lookback is not None:
            params["lookback"] = lookback
        if benchmark_ticker is not None:
            params["benchmark_ticker"] = benchmark_ticker
        return self._get("/api/qdata/v1/stocks/risk-metrics", cast_to=RiskMetricsResponse, options={"params": params})

    def get_market_history(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        interval: str | None = None,
        adj_price: bool | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> MarketHistoryResponse:
        """Retrieves historical market data quotes for a stock.

        Parameters
        ----------
        symbol : str
            Target stock ticker.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        interval : str, optional
            Interval size (e.g. 1d).
        adj_price : bool, optional
            Whether to use adjusted price.
        start : str, optional
            ISO-8601 start date.
        end : str, optional
            ISO-8601 end date.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if interval is not None:
            params["interval"] = interval
        if adj_price is not None:
            params["adj_price"] = adj_price
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._get("/api/qdata/v1/stocks/market", cast_to=MarketHistoryResponse, options={"params": params})

    def get_quote(self, *, symbols: List[str] | None = None) -> CurrentQuoteResponse:
        """Retrieves the current quote pricing for a list of stocks.

        Parameters
        ----------
        symbols : list of str, optional
            Specific stock tickers to query.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return self._get("/api/qdata/v1/stocks/current_quote", cast_to=CurrentQuoteResponse, options={"params": params})

    def post_quote(self, *, body: dict[str, Any]) -> CurrentQuoteResponse:
        """Submits a payload to retrieve stock quotes.

        Parameters
        ----------
        body : dict
            Request body payload (e.g. containing stock lists).
        """
        return self._post("/api/qdata/v1/stocks/current_quote", cast_to=CurrentQuoteResponse, options={"json": body})

    def get_financials(
        self,
        *,
        symbol: str | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> FinancialsResponse:
        """Retrieves fundamentals financial records for a stock.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker.
        lookback : int, optional
            Lookback period size.
        start_date : str, optional
            ISO-8601 start date.
        end_date : str, optional
            ISO-8601 end date.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if lookback is not None:
            params["lookback"] = lookback
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return self._get("/api/qdata/v1/stocks/financials", cast_to=FinancialsResponse, options={"params": params})

    def get_history_quote(
        self,
        *,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> MarketHistoryResponse:
        """Retrieves history quotes for a stock.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max records.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/stocks/history_quote", cast_to=MarketHistoryResponse, options={"params": params})

    def get_info(self, *, symbol: str | None = None) -> StockInfoResponse:
        """Retrieves general stock basic info.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker symbol.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        return self._get("/api/qdata/v1/stocks", cast_to=StockInfoResponse, options={"params": params})

    def get_news(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
    ) -> StockNewsResponse:
        """Retrieves news articles related to a stock.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        return self._get("/api/qdata/v1/stocks/news", cast_to=StockNewsResponse, options={"params": params})

    def get_sentiments(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
    ) -> StockSentimentResponse:
        """Retrieves sentiment score evaluations for a stock.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        return self._get("/api/qdata/v1/stocks/sentiments", cast_to=StockSentimentResponse, options={"params": params})

    def get_ystock_info(
        self,
        *,
        symbols: str | None = None,
        market: str | None = None,
        full_exchange_name: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
        only_simple_fields: bool | None = None,
        return_field_list: str | None = None,
    ) -> YStockInfoResponse:
        """Query multi stock trading stock info by market/industry/sector filters or symbols list.

        Parameters
        ----------
        symbols : str, optional
            Multi symbol separated by comma.
        market : str, optional
            Stock market, e.g., cn/us/hk.
        full_exchange_name : str, optional
            Full exchange name.
        sector : str, optional
            Sector name.
        industry : str, optional
            Industry name.
        only_simple_fields : bool, optional
            Return only standard basic fields if True.
        return_field_list : str, optional
            Specify return fields separated by comma.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        if market is not None:
            params["market"] = market
        if full_exchange_name is not None:
            params["full_exchange_name"] = full_exchange_name
        if sector is not None:
            params["sector"] = sector
        if industry is not None:
            params["industry"] = industry
        if only_simple_fields is not None:
            params["only_simple_fields"] = only_simple_fields
        if return_field_list is not None:
            params["return_field_list"] = return_field_list
        return self._get("/api/qdata/v1/stock/ystock_info", cast_to=YStockInfoResponse, options={"params": params})

    def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        price_adj_type: str | None = None,
        price_adj_date: str | None = None,
        limit: int | None = None,
    ) -> StockKlineResponse:
        """Query single stock daily K-line time series with price adjustments.

        Parameters
        ----------
        symbol : str
            Target stock ticker.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        price_adj_type : str, optional
            Adjustment type: pre, post, or none.
        price_adj_date : str, optional
            Adjustment reference date.
        limit : int, optional
            Max record limit.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if price_adj_type is not None:
            params["price_adj_type"] = price_adj_type
        if price_adj_date is not None:
            params["price_adj_date"] = price_adj_date
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/stock/kline", cast_to=StockKlineResponse, options={"params": params})

    def get_kline_cs(
        self,
        *,
        market: str | None = None,
        symbol_suffix: str | None = None,
        symbols: str | None = None,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        window_limit: int | None = None,
    ) -> StockKlineCSResponse:
        """Query stock daily K-line cross sectional data.

        Parameters
        ----------
        market : str, optional
            Target market code.
        symbol_suffix : str, optional
            Suffix filter for symbols.
        symbols : str, optional
            Multi symbol separated by comma.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        window_limit : int, optional
            Number of recent bars per stock.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if symbol_suffix is not None:
            params["symbol_suffix"] = symbol_suffix
        if symbols is not None:
            params["symbols"] = symbols
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if window_limit is not None:
            params["window_limit"] = window_limit
        return self._get("/api/qdata/v1/stock/kline_cs", cast_to=StockKlineCSResponse, options={"params": params})

    def get_market_summary(self) -> StockMarketSummaryResponse:
        """Retrieves valuation market summaries across different stock markets."""
        return self._get("/api/qdata/v1/stock/market_summary", cast_to=StockMarketSummaryResponse)

    def get_sector_industry_summary(self) -> StockSectorIndustrySummaryResponse:
        """Retrieves industry/sector valuation comparison summaries."""
        return self._get("/api/qdata/v1/stock/sector_industry_summary", cast_to=StockSectorIndustrySummaryResponse)

    def get_kline_interval_stat(
        self,
        *,
        market: str | None = None,
        symbol_suffix: str | None = None,
        symbols: str | None = None,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        window_limit: int | None = None,
    ) -> StockKlineIntervalStatResponse:
        """Query stock daily K-line cross sectional interval statistics.

        Parameters
        ----------
        market : str, optional
            Target market code.
        symbol_suffix : str, optional
            Suffix filter for symbols.
        symbols : str, optional
            Multi symbol separated by comma.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        window_limit : int, optional
            Number of recent bars per stock.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if symbol_suffix is not None:
            params["symbol_suffix"] = symbol_suffix
        if symbols is not None:
            params["symbols"] = symbols
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if window_limit is not None:
            params["window_limit"] = window_limit
        return self._get("/api/qdata/v1/stock/kline_interval_stat", cast_to=StockKlineIntervalStatResponse, options={"params": params})

    def get_stocks_market_summary(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        interval: str | None = None,
        adj_price: bool | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> StocksMarketSummaryResponse:
        """Retrieve stock historical price, volume and other market data summary.

        Parameters
        ----------
        symbol : str
            Stock ticker symbol (e.g., 'AAPL').
        page : int, optional
            Page number for pagination.
        size : int, optional
            Number of items per page.
        limit : int, optional
            Maximum number of records to return.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort order: 'ASC' or 'DESC'.
        include_fields : list of str, optional
            List of specific fields to include.
        interval : str, optional
            Time interval for market data bars.
        adj_price : bool, optional
            Whether to return price-adjusted data.
        start : str, optional
            Start date for historical data.
        end : str, optional
            End date for historical data.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if interval is not None:
            params["interval"] = interval
        if adj_price is not None:
            params["adj_price"] = adj_price
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return self._get("/api/qdata/v1/stocks/market-summary", cast_to=StocksMarketSummaryResponse, options={"params": params})


class AsyncStocks(AsyncAPIResource):

    async def get_competitors(self, *, symbol: str, limit: int | None = None) -> CompetitorsResponse:
        """Retrieves competitor symbols list for a stock asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol (e.g. AAPL).
        limit : int, optional
            Max competitors count.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/stocks/competitors", cast_to=CompetitorsResponse, options={"params": params})

    async def get_risk_metrics(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        lookback: int | None = None,
        benchmark_ticker: str | None = None,
    ) -> RiskMetricsResponse:
        """Retrieves risk metrics for a stock asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        lookback : int, optional
            Lookback period length.
        benchmark_ticker : str, optional
            Ticker to calculate beta against.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if lookback is not None:
            params["lookback"] = lookback
        if benchmark_ticker is not None:
            params["benchmark_ticker"] = benchmark_ticker
        return await self._get("/api/qdata/v1/stocks/risk-metrics", cast_to=RiskMetricsResponse, options={"params": params})

    async def get_market_history(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        interval: str | None = None,
        adj_price: bool | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> MarketHistoryResponse:
        """Retrieves historical market data quotes asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        interval : str, optional
            Interval size.
        adj_price : bool, optional
            Whether to use adjusted price.
        start : str, optional
            ISO-8601 start date.
        end : str, optional
            ISO-8601 end date.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if interval is not None:
            params["interval"] = interval
        if adj_price is not None:
            params["adj_price"] = adj_price
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return await self._get("/api/qdata/v1/stocks/market", cast_to=MarketHistoryResponse, options={"params": params})

    async def get_quote(self, *, symbols: List[str] | None = None) -> CurrentQuoteResponse:
        """Retrieves the current quote pricing asynchronously.

        Parameters
        ----------
        symbols : list of str, optional
            Specific stock tickers to query.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return await self._get("/api/qdata/v1/stocks/current_quote", cast_to=CurrentQuoteResponse, options={"params": params})

    async def post_quote(self, *, body: dict[str, Any]) -> CurrentQuoteResponse:
        """Submits a payload to retrieve stock quotes asynchronously.

        Parameters
        ----------
        body : dict
            Request body payload.
        """
        return await self._post("/api/qdata/v1/stocks/current_quote", cast_to=CurrentQuoteResponse, options={"json": body})

    async def get_financials(
        self,
        *,
        symbol: str | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> FinancialsResponse:
        """Retrieves fundamentals financial records asynchronously.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker.
        lookback : int, optional
            Lookback period size.
        start_date : str, optional
            ISO-8601 start date.
        end_date : str, optional
            ISO-8601 end date.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if lookback is not None:
            params["lookback"] = lookback
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._get("/api/qdata/v1/stocks/financials", cast_to=FinancialsResponse, options={"params": params})

    async def get_history_quote(
        self,
        *,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> MarketHistoryResponse:
        """Retrieves history quotes for a stock asynchronously.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max records.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/stocks/history_quote", cast_to=MarketHistoryResponse, options={"params": params})

    async def get_info(self, *, symbol: str | None = None) -> StockInfoResponse:
        """Retrieves general stock basic info asynchronously.

        Parameters
        ----------
        symbol : str, optional
            Target stock ticker symbol.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        return await self._get("/api/qdata/v1/stocks", cast_to=StockInfoResponse, options={"params": params})

    async def get_news(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
    ) -> StockNewsResponse:
        """Retrieves news articles related to a stock asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        return await self._get("/api/qdata/v1/stocks/news", cast_to=StockNewsResponse, options={"params": params})

    async def get_sentiments(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
    ) -> StockSentimentResponse:
        """Retrieves sentiment score evaluations asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker symbol.
        page : int, optional
            Page number.
        size : int, optional
            Elements per page.
        limit : int, optional
            Max records.
        order_by : str, optional
            Sorting field.
        order_type : str, optional
            Sort direction.
        include_fields : list of str, optional
            Specific fields to return.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        return await self._get("/api/qdata/v1/stocks/sentiments", cast_to=StockSentimentResponse, options={"params": params})

    async def get_ystock_info(
        self,
        *,
        symbols: str | None = None,
        market: str | None = None,
        full_exchange_name: str | None = None,
        sector: str | None = None,
        industry: str | None = None,
        only_simple_fields: bool | None = None,
        return_field_list: str | None = None,
    ) -> YStockInfoResponse:
        """Query multi stock trading stock info by market/industry/sector filters or symbols list asynchronously.

        Parameters
        ----------
        symbols : str, optional
            Multi symbol separated by comma.
        market : str, optional
            Stock market, e.g., cn/us/hk.
        full_exchange_name : str, optional
            Full exchange name.
        sector : str, optional
            Sector name.
        industry : str, optional
            Industry name.
        only_simple_fields : bool, optional
            Return only standard basic fields if True.
        return_field_list : str, optional
            Specify return fields separated by comma.
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        if market is not None:
            params["market"] = market
        if full_exchange_name is not None:
            params["full_exchange_name"] = full_exchange_name
        if sector is not None:
            params["sector"] = sector
        if industry is not None:
            params["industry"] = industry
        if only_simple_fields is not None:
            params["only_simple_fields"] = only_simple_fields
        if return_field_list is not None:
            params["return_field_list"] = return_field_list
        return await self._get("/api/qdata/v1/stock/ystock_info", cast_to=YStockInfoResponse, options={"params": params})

    async def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        price_adj_type: str | None = None,
        price_adj_date: str | None = None,
        limit: int | None = None,
    ) -> StockKlineResponse:
        """Query single stock daily K-line time series with price adjustments asynchronously.

        Parameters
        ----------
        symbol : str
            Target stock ticker.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        price_adj_type : str, optional
            Adjustment type: pre, post, or none.
        price_adj_date : str, optional
            Adjustment reference date.
        limit : int, optional
            Max record limit.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if price_adj_type is not None:
            params["price_adj_type"] = price_adj_type
        if price_adj_date is not None:
            params["price_adj_date"] = price_adj_date
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/stock/kline", cast_to=StockKlineResponse, options={"params": params})

    async def get_kline_cs(
        self,
        *,
        market: str | None = None,
        symbol_suffix: str | None = None,
        symbols: str | None = None,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        window_limit: int | None = None,
    ) -> StockKlineCSResponse:
        """Query stock daily K-line cross sectional data asynchronously.

        Parameters
        ----------
        market : str, optional
            Target market code.
        symbol_suffix : str, optional
            Suffix filter for symbols.
        symbols : str, optional
            Multi symbol separated by comma.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        window_limit : int, optional
            Number of recent bars per stock.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if symbol_suffix is not None:
            params["symbol_suffix"] = symbol_suffix
        if symbols is not None:
            params["symbols"] = symbols
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if window_limit is not None:
            params["window_limit"] = window_limit
        return await self._get("/api/qdata/v1/stock/kline_cs", cast_to=StockKlineCSResponse, options={"params": params})

    async def get_market_summary(self) -> StockMarketSummaryResponse:
        """Retrieves valuation market summaries across different stock markets asynchronously."""
        return await self._get("/api/qdata/v1/stock/market_summary", cast_to=StockMarketSummaryResponse)

    async def get_sector_industry_summary(self) -> StockSectorIndustrySummaryResponse:
        """Retrieves industry/sector valuation comparison summaries asynchronously."""
        return await self._get("/api/qdata/v1/stock/sector_industry_summary", cast_to=StockSectorIndustrySummaryResponse)

    async def get_kline_interval_stat(
        self,
        *,
        market: str | None = None,
        symbol_suffix: str | None = None,
        symbols: str | None = None,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        window_limit: int | None = None,
    ) -> StockKlineIntervalStatResponse:
        """Query stock daily K-line cross sectional interval statistics asynchronously.

        Parameters
        ----------
        market : str, optional
            Target market code.
        symbol_suffix : str, optional
            Suffix filter for symbols.
        symbols : str, optional
            Multi symbol separated by comma.
        kline_t : str, optional
            Bar interval duration.
        start_time : str, optional
            Start time window.
        end_time : str, optional
            End time window.
        window_limit : int, optional
            Number of recent bars per stock.
        """
        params: dict[str, Any] = {}
        if market is not None:
            params["market"] = market
        if symbol_suffix is not None:
            params["symbol_suffix"] = symbol_suffix
        if symbols is not None:
            params["symbols"] = symbols
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if window_limit is not None:
            params["window_limit"] = window_limit
        return await self._get("/api/qdata/v1/stock/kline_interval_stat", cast_to=StockKlineIntervalStatResponse, options={"params": params})

    async def get_stocks_market_summary(
        self,
        *,
        symbol: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        interval: str | None = None,
        adj_price: bool | None = None,
        start: str | None = None,
        end: str | None = None,
    ) -> StocksMarketSummaryResponse:
        """Retrieve stock historical price, volume and other market data summary asynchronously.

        Parameters
        ----------
        symbol : str
            Stock ticker symbol (e.g., 'AAPL').
        page : int, optional
            Page number for pagination.
        size : int, optional
            Number of items per page.
        limit : int, optional
            Maximum number of records to return.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort order: 'ASC' or 'DESC'.
        include_fields : list of str, optional
            List of specific fields to include.
        interval : str, optional
            Time interval for market data bars.
        adj_price : bool, optional
            Whether to return price-adjusted data.
        start : str, optional
            Start date for historical data.
        end : str, optional
            End date for historical data.
        """
        params: dict[str, Any] = {"symbol": symbol}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if limit is not None:
            params["limit"] = limit
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if include_fields is not None:
            params["include_fields"] = include_fields
        if interval is not None:
            params["interval"] = interval
        if adj_price is not None:
            params["adj_price"] = adj_price
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        return await self._get("/api/qdata/v1/stocks/market-summary", cast_to=StocksMarketSummaryResponse, options={"params": params})
