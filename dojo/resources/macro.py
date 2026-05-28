from __future__ import annotations

from typing import Any, List
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    MacroNewsResponse,
    MacroMetricsResponse,
    MacroSentimentResponse,
)


# --- Sync Macro Sub-resources ---
class MacroNews(SyncAPIResource):

    def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        keywords: List[str] | None = None,
        sector: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroNewsResponse:
        """Retrieves macroeconomic news articles.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        keywords : list of str, optional
            Fuzzy matching keyword strings.
        sector : str, optional
            Filter news by macro sector.
        start_date : str, optional
            Filter news on or after a start date.
        end_date : str, optional
            Filter news on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if keywords is not None:
            params["keywords"] = keywords
        if sector is not None:
            params["sector"] = sector
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return self._get("/api/qdata/v1/macro/news", cast_to=MacroNewsResponse, options={"params": params})


class MacroMetrics(SyncAPIResource):

    def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        indicator_key: str | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroMetricsResponse:
        """Retrieves macroeconomic indicator metrics.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        indicator_key : str, optional
            Specific macro indicator key to filter (e.g. CPI).
        lookback : int, optional
            Lookback window limit size.
        start_date : str, optional
            Filter macro values on or after a start date.
        end_date : str, optional
            Filter macro values on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if indicator_key is not None:
            params["indicator_key"] = indicator_key
        if lookback is not None:
            params["lookback"] = lookback
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return self._get("/api/qdata/v1/macro/metrics", cast_to=MacroMetricsResponse, options={"params": params})


class MacroSentiments(SyncAPIResource):

    def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroSentimentResponse:
        """Retrieves macro-level sentiment scores.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        lookback : int, optional
            Lookback window limit size.
        start_date : str, optional
            Filter sentiments on or after a start date.
        end_date : str, optional
            Filter sentiments on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return self._get("/api/qdata/v1/macro/sentiments", cast_to=MacroSentimentResponse, options={"params": params})


class Macro(SyncAPIResource):

    def __init__(self, client: Any, is_raw: bool = False) -> None:
        super().__init__(client, is_raw=is_raw)
        self.news = MacroNews(client, is_raw=is_raw)
        self.metrics = MacroMetrics(client, is_raw=is_raw)
        self.sentiments = MacroSentiments(client, is_raw=is_raw)


# --- Async Macro Sub-resources ---
class AsyncMacroNews(AsyncAPIResource):

    async def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        keywords: List[str] | None = None,
        sector: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroNewsResponse:
        """Retrieves macroeconomic news articles asynchronously.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        keywords : list of str, optional
            Fuzzy matching keyword strings.
        sector : str, optional
            Filter news by macro sector.
        start_date : str, optional
            Filter news on or after a start date.
        end_date : str, optional
            Filter news on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if keywords is not None:
            params["keywords"] = keywords
        if sector is not None:
            params["sector"] = sector
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._get("/api/qdata/v1/macro/news", cast_to=MacroNewsResponse, options={"params": params})


class AsyncMacroMetrics(AsyncAPIResource):

    async def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        indicator_key: str | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroMetricsResponse:
        """Retrieves macroeconomic indicator metrics asynchronously.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        indicator_key : str, optional
            Specific macro indicator key to filter (e.g. CPI).
        lookback : int, optional
            Lookback window limit size.
        start_date : str, optional
            Filter macro values on or after a start date.
        end_date : str, optional
            Filter macro values on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if indicator_key is not None:
            params["indicator_key"] = indicator_key
        if lookback is not None:
            params["lookback"] = lookback
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._get("/api/qdata/v1/macro/metrics", cast_to=MacroMetricsResponse, options={"params": params})


class AsyncMacroSentiments(AsyncAPIResource):

    async def get(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        lookback: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> MacroSentimentResponse:
        """Retrieves macro-level sentiment scores asynchronously.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records.
        order_by : str, optional
            Field name to sort by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to return.
        lookback : int, optional
            Lookback window limit size.
        start_date : str, optional
            Filter sentiments on or after a start date.
        end_date : str, optional
            Filter sentiments on or before an end date.
        """
        params: dict[str, Any] = {}
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
        if start_date is not None:
            params["start_date"] = start_date
        if end_date is not None:
            params["end_date"] = end_date
        return await self._get("/api/qdata/v1/macro/sentiments", cast_to=MacroSentimentResponse, options={"params": params})


class AsyncMacro(AsyncAPIResource):

    def __init__(self, client: Any, is_raw: bool = False) -> None:
        super().__init__(client, is_raw=is_raw)
        self.news = AsyncMacroNews(client, is_raw=is_raw)
        self.metrics = AsyncMacroMetrics(client, is_raw=is_raw)
        self.sentiments = AsyncMacroSentiments(client, is_raw=is_raw)
