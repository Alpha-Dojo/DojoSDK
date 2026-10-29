from __future__ import annotations

import datetime
from typing import Any

from dojo.resources.base import AsyncAPIResource, SyncAPIResource,normalize_naive_iso_datetime
from dojo.types.models import (
    EtfHoldingsResponse,
    EtfTopHoldingTargetResponse,
    EtfLabelsResponse,
    EtfCategoryResponse
)


class Etf(SyncAPIResource):

    def get_etf_holdings(
        self,
        *,
        symbol: str,
        report_end_date: datetime.datetime | None = None,
        filing_end_date: datetime.datetime | None = None,
        reports_limit: int  = 1,
        top_n: int | None = 10,
    ) -> EtfHoldingsResponse:
        """Retrieves the latest N report periods of ETF holdings, with top N holdings per period.

        Parameters
        ----------
        symbol : str, optional
            ETF symbol(s), multiple symbols separated by comma (e.g. SPY,QQQ).
        report_end_date : datetime.datetime, optional
            Report date upper bound (<=).
        filing_end_date : datetime.datetime, optional
            Filing date upper bound (<=).
        reports_limit : int
            Number of latest report periods per symbol, default 1.
        top_n : int, optional
            Top N holdings per period ranked by pct_value desc; default 10. None means all holdings.
        """
        params: dict[str, Any] = {"symbol":symbol,"reports_limit":reports_limit}
        if report_end_date is not None:
            params["report_end_date"] = normalize_naive_iso_datetime(report_end_date)
        if filing_end_date is not None:
            params["filing_end_date"] = normalize_naive_iso_datetime(filing_end_date)
        if top_n is not None:
            params["top_n"] = top_n
        return self._get(
            "/api/qdata/v1/etf/holdings",
            cast_to=EtfHoldingsResponse,
            options={"params": params},
        )

    def get_etfs_by_top_holding(
        self,
        *,
        holding_ticker: str = "NVDA",
        top_n: int = 1,
        report_end_date: datetime.datetime | None = None,
        reports_limit: int = 1,
        limit: int | None = 100,
    ) -> EtfTopHoldingTargetResponse:
        """Finds ETFs whose top holdings include the target ticker.

        Parameters
        ----------
        holding_ticker : str, optional
            Target holding ticker, default 'NVDA'.
        top_n : int, optional
            Holding rank upper bound (1 means the largest holding), default 1.
        report_end_date : datetime.datetime, optional
            Report date upper bound (<=).
        reports_limit : int, optional
            Number of latest report periods to look back, default 1.
        limit : int, optional
            Max number of rows to return after ranking, default 100, order by holding usd value desc.
        """
        params: dict[str, Any] = {
            "holding_ticker": holding_ticker,
            "top_n": top_n,
            "reports_limit": reports_limit,
        }
        if report_end_date is not None:
            params["report_end_date"] = normalize_naive_iso_datetime(report_end_date)
        if limit is not None:
            params["limit"] = limit
        return self._get(
            "/api/qdata/v1/etf/top_holding_target",
            cast_to=EtfTopHoldingTargetResponse,
            options={"params": params},
        )

    def get_etf_labels(
        self,
        *,
        ticker: str | None = None,
        market: str | None = None,
        subcategory_code: str | None = None,
        category_code: str | None = None,
        belong_type: str | None = None,
    ) -> EtfLabelsResponse:
        """Query ETF labels.

        Parameters
        ----------
        ticker : str, optional
            ETF ticker(s), multiple tickers separated by comma (e.g. 'SPY,QQQ,IWM').
        market : str, optional
            Market code, e.g. 'US', 'CN', 'HK'. Exact match.
        subcategory_code : str, optional
            Sub-category code, e.g. '0101'. Exact match.
        category_code : str, optional
            Top-level category code, e.g. '01'. Exact match.
        belong_type : str, optional
            Belong type label. Exact match.
        """
        params: dict[str, Any] = {}
        if ticker is not None:
            params["ticker"] = ticker
        if market is not None:
            params["market"] = market
        if subcategory_code is not None:
            params["subcategory_code"] = subcategory_code
        if category_code is not None:
            params["category_code"] = category_code
        if belong_type is not None:
            params["belong_type"] = belong_type
        return self._get(
            "/api/qdata/v1/etf/labels",
            cast_to=EtfLabelsResponse,
            options={"params": params},
        )

    def get_etf_categories(
        self,
        *,
        category_code: str | None = None,
        parent_code: str | None = None,
        level: int | None = None,
    ) -> EtfCategoryResponse:
        """Query ETF category dictionary (self-referencing tree).

        Parameters
        ----------
        category_code : str, optional
            Category code(s), multiple codes separated by comma (e.g. '01,0101,0102').
        parent_code : str, optional
            Parent category code, e.g. '01' to list its children. Exact match.
        level : int, optional
            Category level: 1 for top level, 2 for sub level. Exact match.
        """
        params: dict[str, Any] = {}
        if category_code is not None:
            params["category_code"] = category_code
        if parent_code is not None:
            params["parent_code"] = parent_code
        if level is not None:
            params["level"] = level
        return self._get(
            "/api/qdata/v1/etf/categories",
            cast_to=EtfCategoryResponse,
            options={"params": params},
        )

class AsyncEtf(AsyncAPIResource):

    async def get_etf_holdings(
        self,
        *,
        symbol: str,
        report_end_date: datetime.datetime | None = None,
        filing_end_date: datetime.datetime | None = None,
        reports_limit: int  = 1,
        top_n: int | None = 10,
    ) -> EtfHoldingsResponse:
        """Retrieves the latest N report periods of ETF holdings, with top N holdings per period.

        Parameters
        ----------
        symbol : str, optional
            ETF symbol(s), multiple symbols separated by comma (e.g. SPY,QQQ).
        report_end_date : datetime.datetime, optional
            Report date upper bound (<=).
        filing_end_date : datetime.datetime, optional
            Filing date upper bound (<=).
        reports_limit : int
            Number of latest report periods per symbol, default 1.
        top_n : int, optional
            Top N holdings per period ranked by pct_value desc; default 10. None means all holdings.
        """
        params: dict[str, Any] = {"symbol":symbol,"reports_limit":reports_limit}
        if report_end_date is not None:
            params["report_end_date"] = normalize_naive_iso_datetime(report_end_date)
        if filing_end_date is not None:
            params["filing_end_date"] = normalize_naive_iso_datetime(filing_end_date)
        if top_n is not None:
            params["top_n"] = top_n
        return await self._get(
            "/api/qdata/v1/etf/holdings",
            cast_to=EtfHoldingsResponse,
            options={"params": params},
        )

    async def get_etfs_by_top_holding(
        self,
        *,
        holding_ticker: str = "NVDA",
        top_n: int = 1,
        report_end_date: datetime.datetime | None = None,
        reports_limit: int = 1,
        limit: int | None = 100,
    ) -> EtfTopHoldingTargetResponse:
        """Finds ETFs whose top holdings include the target ticker.

        Parameters
        ----------
        holding_ticker : str, optional
            Target holding ticker, default 'NVDA'.
        top_n : int, optional
            Holding rank upper bound (1 means the largest holding), default 1.
        report_end_date : datetime.datetime, optional
            Report date upper bound (<=).
        reports_limit : int, optional
            Number of latest report periods to look back, default 1.
        limit : int, optional
            Max number of rows to return after ranking, default 100, order by holding usd value desc.
        """
        params: dict[str, Any] = {
            "holding_ticker": holding_ticker,
            "top_n": top_n,
            "reports_limit": reports_limit,
        }
        if report_end_date is not None:
            params["report_end_date"] = normalize_naive_iso_datetime(report_end_date)
        if limit is not None:
            params["limit"] = limit
        return await self._get(
            "/api/qdata/v1/etf/top_holding_target",
            cast_to=EtfTopHoldingTargetResponse,
            options={"params": params},
        )

    async def get_etf_labels(
        self,
        *,
        ticker: str | None = None,
        market: str | None = None,
        subcategory_code: str | None = None,
        category_code: str | None = None,
        belong_type: str | None = None,
    ) -> EtfLabelsResponse:
        """Query ETF labels asynchronously.

        See ``ETF.get_etf_labels`` for parameter details.
        """
        params: dict[str, Any] = {}
        if ticker is not None:
            params["ticker"] = ticker
        if market is not None:
            params["market"] = market
        if subcategory_code is not None:
            params["subcategory_code"] = subcategory_code
        if category_code is not None:
            params["category_code"] = category_code
        if belong_type is not None:
            params["belong_type"] = belong_type
        return await self._get(
            "/api/qdata/v1/etf/labels",
            cast_to=EtfLabelsResponse,
            options={"params": params},
        )

    async def get_etf_categories(
        self,
        *,
        category_code: str | None = None,
        parent_code: str | None = None,
        level: int | None = None,
    ) -> EtfCategoryResponse:
        """Query ETF category dictionary asynchronously.

        See ``ETF.get_etf_categories`` for parameter details.
        """
        params: dict[str, Any] = {}
        if category_code is not None:
            params["category_code"] = category_code
        if parent_code is not None:
            params["parent_code"] = parent_code
        if level is not None:
            params["level"] = level
        return await self._get(
            "/api/qdata/v1/etf/categories",
            cast_to=EtfCategoryResponse,
            options={"params": params},
        )
