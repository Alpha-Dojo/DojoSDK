from __future__ import annotations

from typing import Any, List
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    BasicInfoResponse,
    TickerResponse,
    DepthResponse,
    KLineResponse,
    MarkPriceResponse,
    FundingRateResponse,
    TopLongShortResponse,
    VolatilityResponse,
    IndicatorResponse,
    IndicesResponse,
    InstrumentsResponse,
)


class MarketData(SyncAPIResource):

    def get_basic_info(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbols: List[str] | None = None,
        limit: int | None = None,
    ) -> BasicInfoResponse:
        """Retrieves exchange tradable symbols information.

        Parameters
        ----------
        exchange : str
            The name of the exchange (e.g. BINANCE).
        bz_type : str
            The business type (e.g. SPOT, SWAP).
        symbols : list of str, optional
            List of specific symbols to query.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        BasicInfoResponse
            The basic info response containing symbol details.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbols is not None:
            params["symbols"] = symbols
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/basic_info", cast_to=BasicInfoResponse, options={"params": params})

    def get_ticker(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> TickerResponse:
        """Retrieves real-time ticker data with 24-hour price and volume statistics.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific ticker symbol to query.
        end_time : str, optional
            Filter data up to this end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        TickerResponse
            Ticker statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/ticker", cast_to=TickerResponse, options={"params": params})

    def get_depth(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> DepthResponse:
        """Retrieves real-time orderbook depth data with limited history.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to query.
        end_time : str, optional
            Filter data up to this end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        DepthResponse
            Orderbook depth response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/depth", cast_to=DepthResponse, options={"params": params})

    def get_kline(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        limit: int | None = None,
    ) -> KLineResponse:
        """Retrieves historical kline (candlestick) data.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to query.
        kline_t : str, optional
            Kline interval (e.g. 1m, 5m, 1h, 1d).
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        KLineResponse
            Kline historical data response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/kline", cast_to=KLineResponse, options={"params": params})

    def get_mark_price(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> MarkPriceResponse:
        """Retrieves real-time mark price data and funding rate index.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol to query.
        end_time : str, optional
            ISO-8601 end time filter.
        limit : int, optional
            Maximum records limit.

        Returns
        -------
        MarkPriceResponse
            Real-time mark price statistics.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/mark_price", cast_to=MarkPriceResponse, options={"params": params})

    def get_funding_rate(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        limit: int | None = None,
    ) -> FundingRateResponse:
        """Retrieves historical realized funding rates for perpetual contracts.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol.
        end_time : str, optional
            ISO-8601 end time filter.
        start_time : str, optional
            ISO-8601 start time filter.
        limit : int, optional
            Maximum records.

        Returns
        -------
        FundingRateResponse
            Historical funding rates.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/funding_rate", cast_to=FundingRateResponse, options={"params": params})

    def get_top_longshort(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        period: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> TopLongShortResponse:
        """Retrieves top traders' position long/short ratio and net positions.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol to filter.
        period : str, optional
            Period interval (e.g. 5m, 1h, 1d).
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        TopLongShortResponse
            Top long/short statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if period is not None:
            params["period"] = period
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/top_longshort", cast_to=TopLongShortResponse, options={"params": params})

    def get_volatility(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        rolling_window: int | None = None,
        limit: int | None = None,
    ) -> VolatilityResponse:
        """Retrieves rolling historical volatility calculated from klines.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol.
        kline_t : str, optional
            Kline interval.
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        rolling_window : int, optional
            Rolling window size for calculating statistics.
        limit : int, optional
            Maximum records.

        Returns
        -------
        VolatilityResponse
            Volatility stats response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if rolling_window is not None:
            params["rolling_window"] = rolling_window
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/volatility", cast_to=VolatilityResponse, options={"params": params})

    def get_indicator(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        indicator: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        rolling_window: int | None = None,
        limit: int | None = None,
    ) -> IndicatorResponse:
        """Retrieves rolling factor indicators calculated based on klines.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to filter.
        indicator : str, optional
            The indicator name (e.g. MACD, RSI).
        kline_t : str, optional
            Kline interval size.
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        rolling_window : int, optional
            The window size.
        limit : int, optional
            Maximum records to return.

        Returns
        -------
        IndicatorResponse
            Calculated factor indicator statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if indicator is not None:
            params["indicator"] = indicator
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if rolling_window is not None:
            params["rolling_window"] = rolling_window
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/indicator", cast_to=IndicatorResponse, options={"params": params})


class AsyncMarketData(AsyncAPIResource):

    async def get_basic_info(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbols: List[str] | None = None,
        limit: int | None = None,
    ) -> BasicInfoResponse:
        """Retrieves exchange tradable symbols information asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange (e.g. BINANCE).
        bz_type : str
            The business type (e.g. SPOT, SWAP).
        symbols : list of str, optional
            List of specific symbols to query.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        BasicInfoResponse
            The basic info response containing symbol details.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbols is not None:
            params["symbols"] = symbols
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/basic_info", cast_to=BasicInfoResponse, options={"params": params})

    async def get_ticker(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> TickerResponse:
        """Retrieves real-time ticker data asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific ticker symbol to query.
        end_time : str, optional
            Filter data up to this end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        TickerResponse
            Ticker statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/ticker", cast_to=TickerResponse, options={"params": params})

    async def get_depth(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> DepthResponse:
        """Retrieves real-time orderbook depth data asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to query.
        end_time : str, optional
            Filter data up to this end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        DepthResponse
            Orderbook depth response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/depth", cast_to=DepthResponse, options={"params": params})

    async def get_kline(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        limit: int | None = None,
    ) -> KLineResponse:
        """Retrieves historical kline (candlestick) data asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to query.
        kline_t : str, optional
            Kline interval (e.g. 1m, 5m, 1h, 1d).
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        KLineResponse
            Kline historical data response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/kline", cast_to=KLineResponse, options={"params": params})

    async def get_mark_price(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> MarkPriceResponse:
        """Retrieves real-time mark price data asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol to query.
        end_time : str, optional
            ISO-8601 end time filter.
        limit : int, optional
            Maximum records limit.

        Returns
        -------
        MarkPriceResponse
            Real-time mark price statistics.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/mark_price", cast_to=MarkPriceResponse, options={"params": params})

    async def get_funding_rate(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        limit: int | None = None,
    ) -> FundingRateResponse:
        """Retrieves historical realized funding rates asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol.
        end_time : str, optional
            ISO-8601 end time filter.
        start_time : str, optional
            ISO-8601 start time filter.
        limit : int, optional
            Maximum records.

        Returns
        -------
        FundingRateResponse
            Historical funding rates.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/funding_rate", cast_to=FundingRateResponse, options={"params": params})

    async def get_top_longshort(
        self,
        *,
        exchange: str,
        bz_type: str | None = None,
        symbol: str | None = None,
        period: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> TopLongShortResponse:
        """Retrieves top traders' position long/short ratio asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str, optional
            The business type.
        symbol : str, optional
            Specific symbol to filter.
        period : str, optional
            Period interval (e.g. 5m, 1h, 1d).
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of records to return.

        Returns
        -------
        TopLongShortResponse
            Top long/short statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange}
        if bz_type is not None:
            params["bz_type"] = bz_type
        if symbol is not None:
            params["symbol"] = symbol
        if period is not None:
            params["period"] = period
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/top_longshort", cast_to=TopLongShortResponse, options={"params": params})

    async def get_volatility(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        rolling_window: int | None = None,
        limit: int | None = None,
    ) -> VolatilityResponse:
        """Retrieves rolling historical volatility asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol.
        kline_t : str, optional
            Kline interval.
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        rolling_window : int, optional
            Rolling window size for calculating statistics.
        limit : int, optional
            Maximum records.

        Returns
        -------
        VolatilityResponse
            Volatility stats response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if rolling_window is not None:
            params["rolling_window"] = rolling_window
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/volatility", cast_to=VolatilityResponse, options={"params": params})

    async def get_indicator(
        self,
        *,
        exchange: str,
        bz_type: str,
        symbol: str | None = None,
        indicator: str | None = None,
        kline_t: str | None = None,
        end_time: str | None = None,
        start_time: str | None = None,
        rolling_window: int | None = None,
        limit: int | None = None,
    ) -> IndicatorResponse:
        """Retrieves rolling factor indicators asynchronously.

        Parameters
        ----------
        exchange : str
            The name of the exchange.
        bz_type : str
            The business type.
        symbol : str, optional
            Specific symbol to filter.
        indicator : str, optional
            The indicator name.
        kline_t : str, optional
            Kline interval size.
        end_time : str, optional
            ISO-8601 end time.
        start_time : str, optional
            ISO-8601 start time.
        rolling_window : int, optional
            The window size.
        limit : int, optional
            Maximum records to return.

        Returns
        -------
        IndicatorResponse
            Calculated factor indicator statistics response.
        """
        params: dict[str, Any] = {"exchange": exchange, "bz_type": bz_type}
        if symbol is not None:
            params["symbol"] = symbol
        if indicator is not None:
            params["indicator"] = indicator
        if kline_t is not None:
            params["kline_t"] = kline_t
        if end_time is not None:
            params["end_time"] = end_time
        if start_time is not None:
            params["start_time"] = start_time
        if rolling_window is not None:
            params["rolling_window"] = rolling_window
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/indicator", cast_to=IndicatorResponse, options={"params": params})


# --- Helper resource classes Indices and Instruments ---
class Indices(SyncAPIResource):

    def get(self, *, symbol: str | None = None) -> IndicesResponse:
        """Retrieves index info.

        Parameters
        ----------
        symbol : str, optional
            Specific index symbol to query.

        Returns
        -------
        IndicesResponse
            Index details response.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        return self._get("/api/qdata/v1/indices", cast_to=IndicesResponse, options={"params": params})


class AsyncIndices(AsyncAPIResource):

    async def get(self, *, symbol: str | None = None) -> IndicesResponse:
        """Retrieves index info asynchronously.

        Parameters
        ----------
        symbol : str, optional
            Specific index symbol to query.

        Returns
        -------
        IndicesResponse
            Index details response.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        return await self._get("/api/qdata/v1/indices", cast_to=IndicesResponse, options={"params": params})


class Instruments(SyncAPIResource):

    def get(
        self,
        *,
        symbol: str | None = None,
        category: str | None = None,
        subcategory: str | None = None,
        industry: str | None = None,
        sector: str | None = None,
    ) -> InstrumentsResponse:
        """Retrieves listing of instruments details.

        Parameters
        ----------
        symbol : str, optional
            Specific instrument ticker symbol.
        category : str, optional
            Category name to filter.
        subcategory : str, optional
            Subcategory name to filter.
        industry : str, optional
            Industry name to filter.
        sector : str, optional
            Sector name to filter.

        Returns
        -------
        InstrumentsResponse
            Instruments listings response.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        return self._get("/api/qdata/v1/instruments", cast_to=InstrumentsResponse, options={"params": params})


class AsyncInstruments(AsyncAPIResource):

    async def get(
        self,
        *,
        symbol: str | None = None,
        category: str | None = None,
        subcategory: str | None = None,
        industry: str | None = None,
        sector: str | None = None,
    ) -> InstrumentsResponse:
        """Retrieves listing of instruments details asynchronously.

        Parameters
        ----------
        symbol : str, optional
            Specific instrument ticker symbol.
        category : str, optional
            Category name to filter.
        subcategory : str, optional
            Subcategory name to filter.
        industry : str, optional
            Industry name to filter.
        sector : str, optional
            Sector name to filter.

        Returns
        -------
        InstrumentsResponse
            Instruments listings response.
        """
        params: dict[str, Any] = {}
        if symbol is not None:
            params["symbol"] = symbol
        if category is not None:
            params["category"] = category
        if subcategory is not None:
            params["subcategory"] = subcategory
        if industry is not None:
            params["industry"] = industry
        if sector is not None:
            params["sector"] = sector
        return await self._get("/api/qdata/v1/instruments", cast_to=InstrumentsResponse, options={"params": params})
