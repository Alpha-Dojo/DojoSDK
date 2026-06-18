from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    NewsResponse,
    NewsScoreResponse,
    NewsTitleResponse,
    StockEventResponse,
    ExternalEventsResponse,
    ExternalEventRelatedNodesResponse,
)


class News(SyncAPIResource):

    def get_news(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        topic: str | None = None,
        limit: int | None = None,
    ) -> NewsResponse:
        """Retrieves financial and economic news articles.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-05-28T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        topic : str, optional
            Topic name filter.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if topic is not None:
            params["topic"] = topic
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/news", cast_to=NewsResponse, options={"params": params})

    def get_sentiment_score(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> NewsScoreResponse:
        """Retrieves sentiment score evaluations on finance/crypto news.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/news_score", cast_to=NewsScoreResponse, options={"params": params})

    def get_titles(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        topic: str | None = None,
        limit: int | None = None,
    ) -> NewsTitleResponse:
        """Retrieves title feeds for financial news.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        topic : str, optional
            Filter titles by topic key.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if topic is not None:
            params["topic"] = topic
        if limit is not None:
            params["limit"] = limit
        return self._get("/api/qdata/v1/news_title", cast_to=NewsTitleResponse, options={"params": params})

    def get_events(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        fuzzy: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        source_type: str | None = None,
    ) -> StockEventResponse:
        """Retrieves global live news events.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        order_by : str, optional
            Field to order by.
        order_type : str, optional
            Sort direction (asc or desc).
        fuzzy : str, optional
            Fuzzy matching query.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        source_type : str, optional
            The event source filter.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if fuzzy is not None:
            params["fuzzy"] = fuzzy
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if source_type is not None:
            params["source_type"] = source_type
        return self._get("/api/qdata/v1/live_news", cast_to=StockEventResponse, options={"params": params})

    def get_external_events(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        fuzzy: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        source_type: str | None = None,
    ) -> ExternalEventsResponse:
        """Retrieves external global news events.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        order_by : str, optional
            Field to order by.
        order_type : str, optional
            Sort direction (asc or desc).
        fuzzy : str, optional
            Fuzzy matching query.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        source_type : str, optional
            The event source filter.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if fuzzy is not None:
            params["fuzzy"] = fuzzy
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if source_type is not None:
            params["source_type"] = source_type
        return self._get("/api/qdata/v1/external_events", cast_to=ExternalEventsResponse, options={"params": params})

    def get_related_nodes(
        self,
        *,
        source_type: str,
        uq_id: str,
        limit: int | None = None,
    ) -> ExternalEventRelatedNodesResponse:
        """Retrieves related nodes and graph structures for an external event.

        Parameters
        ----------
        source_type : str
            The type of source (e.g. trading_economics, polymarket_event, polymarket_market).
        uq_id : str
            Unique identifier of the event.
        limit : int, optional
            Max records count (default: 50, max: 200, min: 1).
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return self._get(
            f"/api/qdata/v1/external_events/{source_type}/{uq_id}/related_nodes",
            cast_to=ExternalEventRelatedNodesResponse,
            options={"params": params},
        )


class AsyncNews(AsyncAPIResource):

    async def get_news(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        topic: str | None = None,
        limit: int | None = None,
    ) -> NewsResponse:
        """Retrieves financial and economic news articles asynchronously.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time (e.g. 2026-05-28T00:00:00Z).
        end_time : str, optional
            ISO-8601 end time.
        topic : str, optional
            Topic name filter.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if topic is not None:
            params["topic"] = topic
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/news", cast_to=NewsResponse, options={"params": params})

    async def get_sentiment_score(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        limit: int | None = None,
    ) -> NewsScoreResponse:
        """Retrieves sentiment score evaluations on finance/crypto news asynchronously.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/news_score", cast_to=NewsScoreResponse, options={"params": params})

    async def get_titles(
        self,
        *,
        start_time: str | None = None,
        end_time: str | None = None,
        topic: str | None = None,
        limit: int | None = None,
    ) -> NewsTitleResponse:
        """Retrieves title feeds for financial news asynchronously.

        Parameters
        ----------
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        topic : str, optional
            Filter titles by topic key.
        limit : int, optional
            Max number of records to return.
        """
        params: dict[str, Any] = {}
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if topic is not None:
            params["topic"] = topic
        if limit is not None:
            params["limit"] = limit
        return await self._get("/api/qdata/v1/news_title", cast_to=NewsTitleResponse, options={"params": params})

    async def get_events(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        fuzzy: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        source_type: str | None = None,
    ) -> StockEventResponse:
        """Retrieves global live news events asynchronously.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        order_by : str, optional
            Field to order by.
        order_type : str, optional
            Sort direction (asc or desc).
        fuzzy : str, optional
            Fuzzy matching query.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        source_type : str, optional
            The event source filter.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if fuzzy is not None:
            params["fuzzy"] = fuzzy
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if source_type is not None:
            params["source_type"] = source_type
        return await self._get("/api/qdata/v1/live_news", cast_to=StockEventResponse, options={"params": params})

    async def get_external_events(
        self,
        *,
        page: int | None = None,
        size: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        fuzzy: str | None = None,
        start_time: str | None = None,
        end_time: str | None = None,
        source_type: str | None = None,
    ) -> ExternalEventsResponse:
        """Retrieves external global news events asynchronously.

        Parameters
        ----------
        page : int, optional
            Page number.
        size : int, optional
            Number of elements per page.
        order_by : str, optional
            Field to order by.
        order_type : str, optional
            Sort direction (asc or desc).
        fuzzy : str, optional
            Fuzzy matching query.
        start_time : str, optional
            ISO-8601 start time.
        end_time : str, optional
            ISO-8601 end time.
        source_type : str, optional
            The event source filter.
        """
        params: dict[str, Any] = {}
        if page is not None:
            params["page"] = page
        if size is not None:
            params["size"] = size
        if order_by is not None:
            params["order_by"] = order_by
        if order_type is not None:
            params["order_type"] = order_type
        if fuzzy is not None:
            params["fuzzy"] = fuzzy
        if start_time is not None:
            params["start_time"] = start_time
        if end_time is not None:
            params["end_time"] = end_time
        if source_type is not None:
            params["source_type"] = source_type
        return await self._get("/api/qdata/v1/external_events", cast_to=ExternalEventsResponse, options={"params": params})

    async def get_related_nodes(
        self,
        *,
        source_type: str,
        uq_id: str,
        limit: int | None = None,
    ) -> ExternalEventRelatedNodesResponse:
        """Retrieves related nodes and graph structures for an external event asynchronously.

        Parameters
        ----------
        source_type : str
            The type of source (e.g. trading_economics, polymarket_event, polymarket_market).
        uq_id : str
            Unique identifier of the event.
        limit : int, optional
            Max records count (default: 50, max: 200, min: 1).
        """
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            f"/api/qdata/v1/external_events/{source_type}/{uq_id}/related_nodes",
            cast_to=ExternalEventRelatedNodesResponse,
            options={"params": params},
        )
