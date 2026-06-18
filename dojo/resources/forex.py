from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    ForexCurrentQuoteResponse,
    ForexKlineResponse,
    ForexSymbolListResponse,
)


class Forex(SyncAPIResource):

    def get_current_quote(self, *, symbols: str | None = None) -> ForexCurrentQuoteResponse:
        """Retrieves the current quote pricing for forex pairs.

        Parameters
        ----------
        symbols : str, optional
            Multi symbol separated by comma (e.g. EURUSD,USDJPY).
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return self._get("/api/qdata/v1/forex/current_quote", cast_to=ForexCurrentQuoteResponse, options={"params": params})

    def post_current_quote(self, *, body: dict[str, Any]) -> ForexCurrentQuoteResponse:
        """Submits a payload to retrieve forex quotes.

        Parameters
        ----------
        body : dict
            Request body payload (e.g. {"symbols": "EURUSD,USDJPY"}).
        """
        return self._post("/api/qdata/v1/forex/current_quote", cast_to=ForexCurrentQuoteResponse, options={"json": body})

    def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> ForexKlineResponse:
        """Retrieves historical kline (candlestick) data for a forex pair.

        Parameters
        ----------
        symbol : str
            Forex pair symbol (e.g. EURUSD).
        kline_t : str, optional
            Kline interval (e.g. 1m, 5m, 1h, 1d).
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of records to return (max: 5040).
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/forex/kline", cast_to=ForexKlineResponse, options={"params": params})

    kline = get_kline

    def get_symbol_list(self) -> ForexSymbolListResponse:
        """Retrieves the list of available forex symbols."""
        return self._get("/api/qdata/v1/forex/symbol_list", cast_to=ForexSymbolListResponse)


class AsyncForex(AsyncAPIResource):

    async def get_current_quote(self, *, symbols: str | None = None) -> ForexCurrentQuoteResponse:
        """Retrieves the current quote pricing for forex pairs asynchronously.

        Parameters
        ----------
        symbols : str, optional
            Multi symbol separated by comma (e.g. EURUSD,USDJPY).
        """
        params: dict[str, Any] = {}
        if symbols is not None:
            params["symbols"] = symbols
        return await self._get("/api/qdata/v1/forex/current_quote", cast_to=ForexCurrentQuoteResponse, options={"params": params})

    async def post_current_quote(self, *, body: dict[str, Any]) -> ForexCurrentQuoteResponse:
        """Submits a payload to retrieve forex quotes asynchronously.

        Parameters
        ----------
        body : dict
            Request body payload (e.g. {"symbols": "EURUSD,USDJPY"}).
        """
        return await self._post("/api/qdata/v1/forex/current_quote", cast_to=ForexCurrentQuoteResponse, options={"json": body})

    async def get_kline(
        self,
        *,
        symbol: str,
        kline_t: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> ForexKlineResponse:
        """Retrieves historical kline (candlestick) data for a forex pair asynchronously.

        Parameters
        ----------
        symbol : str
            Forex pair symbol (e.g. EURUSD).
        kline_t : str, optional
            Kline interval (e.g. 1m, 5m, 1h, 1d).
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Maximum number of records to return (max: 5040).
        """
        params: dict[str, Any] = {"symbol": symbol}
        if kline_t is not None:
            params["kline_t"] = kline_t
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/forex/kline", cast_to=ForexKlineResponse, options={"params": params})

    kline = get_kline

    async def get_symbol_list(self) -> ForexSymbolListResponse:
        """Retrieves the list of available forex symbols asynchronously."""
        return await self._get("/api/qdata/v1/forex/symbol_list", cast_to=ForexSymbolListResponse)
