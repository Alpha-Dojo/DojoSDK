from __future__ import annotations

from typing import Any, List
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    SectorsResponse,
    SectorMetricsResponse,
    SectorInfoListResponse,
    SectorInfoCreateResponse,
    SectorSymbolRelationListResponse,
    SectorSymbolRelationCreateResponse,
    SectorPrecomputedConstituentsResponse,
    SectorPrecomputedDailyResponse,
    SectorPrecomputedTickerDailyResponse,
    SectorPrecomputedFundamentalsPeriodResponse,
    SectorPrecomputedMarketBenchmarkDailyResponse,
    SectorPrecomputedSectorHorizonMetricsResponse,
    SectorPrecomputedThemeStateDailyResponse,
    SectorPrecomputedSectorAlphaFactorsDailyResponse,
    SectorPrecomputedTickerAlphaFactorsDailyResponse,
    SectorMoversResponse,
)


def _params(**values: Any) -> dict[str, Any]:
    return {name: value for name, value in values.items() if value is not None}


def _daily_params(
    *,
    market: str | None,
    start_date: str | None = None,
    end_date: str | None = None,
    scope: str | None = None,
    level1_id: int | None = None,
    level2_id: int | None = None,
    level3_id: int | None = None,
    ticker: str | None = None,
    role: str | None = None,
    benchmark_id: str | None = None,
    limit: int | None = None,
    offset: int | None = None,
) -> dict[str, Any]:
    return _params(
        market=market,
        start_date=start_date,
        end_date=end_date,
        scope=scope,
        level1_id=level1_id,
        level2_id=level2_id,
        level3_id=level3_id,
        ticker=ticker,
        role=role,
        benchmark_id=benchmark_id,
        limit=limit,
        offset=offset,
    )


class Sectors(SyncAPIResource):

    def get(self) -> SectorsResponse:
        """Retrieves list of all sectors.

        Returns
        -------
        SectorsResponse
            The list of sectors.
        """
        return self._get("/api/qdata/v1/sectors", cast_to=SectorsResponse)

    def get_metrics(
        self,
        *,
        metric_type: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        sector: str | None = None,
        as_of_date: str | None = None,
    ) -> SectorMetricsResponse:
        """Retrieves performance metrics for sectors.

        Parameters
        ----------
        metric_type : str
            The type of metric to retrieve.
        page : int, optional
            Page number for pagination.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records to return.
        order_by : str, optional
            Field name to sort results by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to include in the response.
        sector : str, optional
            Specific sector name to filter by.
        as_of_date : str, optional
            Filter records as of a specific date (e.g. 2026-05-28).
        """
        params: dict[str, Any] = {"metric_type": metric_type}
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
        if sector is not None:
            params["sector"] = sector
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return self._get(
            "/api/qdata/v1/sectors/metrics",
            cast_to=SectorMetricsResponse,
            options={"params": params},
        )

    def get_info(
        self,
        *,
        name: str | None = None,
        name_alias: str | None = None,
        description_alias: str | None = None,
        level: int | None = None,
        parent_id: int | None = None,
        sensitivity: str | None = None,
        tree: bool | None = None,
    ) -> SectorInfoListResponse:
        """Retrieves detailed sector taxonomy information.

        Parameters
        ----------
        name : str, optional
            Sector name.
        name_alias : str, optional
            Sector name alias.
        description_alias : str, optional
            Sector description alias.
        level : int, optional
            Sector hierarchy level.
        parent_id : int, optional
            Parent sector ID.
        sensitivity : str, optional
            Sector sensitivity.
        tree : bool, optional
            Whether to return in tree format (default: False).
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if name_alias is not None:
            params["name_alias"] = name_alias
        if description_alias is not None:
            params["description_alias"] = description_alias
        if level is not None:
            params["level"] = level
        if parent_id is not None:
            params["parent_id"] = parent_id
        if sensitivity is not None:
            params["sensitivity"] = sensitivity
        if tree is not None:
            params["tree"] = tree
        return self._get(
            "/api/qdata/v1/sector/info",
            cast_to=SectorInfoListResponse,
            options={"params": params},
        )

    info = get_info

    def create_info(self, *, body: dict[str, Any]) -> SectorInfoCreateResponse:
        """Creates new sector taxonomy items.

        Parameters
        ----------
        body : dict
            Request body containing items to create.
        """
        return self._post(
            "/api/qdata/v1/sector/info",
            cast_to=SectorInfoCreateResponse,
            options={"json": body},
        )

    def get_symbol_relations(
        self,
        *,
        sector_name: str | None = None,
        symbol: str | None = None,
        relation_priority: str | None = None,
        market: str,
    ) -> SectorSymbolRelationListResponse:
        """Retrieves relationships between sectors and stock/instrument symbols.

        Parameters
        ----------
        sector_name : str, optional
            Sector name to query.
        symbol : str, optional
            Symbol to query.
        relation_priority : str, optional
            Relation priority filter.
        """
        params: dict[str, Any] = {}
        if sector_name is not None:
            params["sector_name"] = sector_name
        if symbol is not None:
            params["symbol"] = symbol
        if relation_priority is not None:
            params["relation_priority"] = relation_priority
        if market is not None:
            params["market"] = market
        return self._get(
            "/api/qdata/v1/sector/symbol_relations",
            cast_to=SectorSymbolRelationListResponse,
            options={"params": params},
        )

    def create_symbol_relations(self, *, body: dict[str, Any]) -> SectorSymbolRelationCreateResponse:
        """Maps symbols to sectors.

        Parameters
        ----------
        body : dict
            Request body containing symbol mappings.
        """
        return self._post(
            "/api/qdata/v1/sector/symbol_relations",
            cast_to=SectorSymbolRelationCreateResponse,
            options={"json": body},
        )

    def get_movers(
        self,
        *,
        market: str | None = None,
        scope: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> SectorMoversResponse:
        return self._get(
            "/api/qdata/v1/sector/movers",
            cast_to=SectorMoversResponse,
            options={"params": _params(market=market, scope=scope, start_date=start_date, end_date=end_date)},
        )

    def get_constituents(
        self,
        *,
        market: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedConstituentsResponse:
        path = "/api/qdata/v1/market/sectors/constituents" if self._client.online else "/api/qdata/v1/sector/precomputed/constituents"
        return self._get(
            path,
            cast_to=SectorPrecomputedConstituentsResponse,
            options={
                "params": _params(
                    market=market,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    def get_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedDailyResponse:
        path = "/api/qdata/v1/market/sectors/daily" if self._client.online else "/api/qdata/v1/sector/precomputed/sector_daily"
        return self._get(
            path,
            cast_to=SectorPrecomputedDailyResponse,
            options={
                "params": _daily_params(
                    market=market,
                    start_date=start_date,
                    end_date=end_date,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    benchmark_id=benchmark_id,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    def get_ticker_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedTickerDailyResponse:
        path = "/api/qdata/v1/market/tickers/daily" if self._client.online else "/api/qdata/v1/sector/precomputed/ticker_daily"
        return self._get(
            path,
            cast_to=SectorPrecomputedTickerDailyResponse,
            options={
                "params": _daily_params(
                    market=market,
                    start_date=start_date,
                    end_date=end_date,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    benchmark_id=benchmark_id,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    def get_fundamentals_periods(
        self,
        *,
        market: str,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        report_period_key: str | None = None,
        limit: int | None = None,
    ) -> SectorPrecomputedFundamentalsPeriodResponse:
        return self._get(
            "/api/qdata/v1/market/sectors/fundamentals/periods",
            cast_to=SectorPrecomputedFundamentalsPeriodResponse,
            options={
                "params": _params(
                    market=market,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    report_period_key=report_period_key,
                    limit=limit,
                )
            },
        )

    def get_horizon_metrics_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedSectorHorizonMetricsResponse:
        params = _daily_params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return self._get(
            "/api/qdata/v1/market/sectors/horizon-metrics/daily",
            cast_to=SectorPrecomputedSectorHorizonMetricsResponse,
            options={"params": params},
        )

    def get_theme_state_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedThemeStateDailyResponse:
        params = _daily_params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return self._get(
            "/api/qdata/v1/market/sectors/theme-state/daily",
            cast_to=SectorPrecomputedThemeStateDailyResponse,
            options={"params": params},
        )

    def get_sector_factors_daily(
        self,
        *,
        market: str,
        level3_id: int,
        rule: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        latest: bool | None = None,
    ) -> SectorPrecomputedSectorAlphaFactorsDailyResponse:
        return self._get(
            "/api/qdata/v1/market/sectors/factors/daily",
            cast_to=SectorPrecomputedSectorAlphaFactorsDailyResponse,
            options={
                "params": _params(
                    market=market,
                    level3_id=level3_id,
                    rule=rule,
                    start_date=start_date,
                    end_date=end_date,
                    latest=latest,
                )
            },
        )

    def get_ticker_factors_daily(
        self,
        *,
        market: str,
        ticker: str,
        rule: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        latest: bool | None = None,
    ) -> SectorPrecomputedTickerAlphaFactorsDailyResponse:
        return self._get(
            "/api/qdata/v1/market/tickers/factors/daily",
            cast_to=SectorPrecomputedTickerAlphaFactorsDailyResponse,
            options={
                "params": _params(
                    market=market,
                    ticker=ticker,
                    rule=rule,
                    start_date=start_date,
                    end_date=end_date,
                    latest=latest,
                )
            },
        )

    def get_precomputed_constituents(self, **kwargs: Any) -> SectorPrecomputedConstituentsResponse:
        return self.get_constituents(**kwargs)

    def get_precomputed_sector_daily(self, **kwargs: Any) -> SectorPrecomputedDailyResponse:
        return self.get_daily(**kwargs)

    def get_precomputed_ticker_daily(self, **kwargs: Any) -> SectorPrecomputedTickerDailyResponse:
        return self.get_ticker_daily(**kwargs)

    def get_precomputed_fundamentals_period(self, **kwargs: Any) -> SectorPrecomputedFundamentalsPeriodResponse:
        return self.get_fundamentals_periods(**kwargs)

    def get_precomputed_market_benchmark_daily(self, **kwargs: Any) -> SectorPrecomputedMarketBenchmarkDailyResponse:
        return self._client.benchmark.get_market_daily(**kwargs)

    def get_precomputed_sector_horizon_metrics(self, **kwargs: Any) -> SectorPrecomputedSectorHorizonMetricsResponse:
        return self.get_horizon_metrics_daily(**kwargs)

    def get_precomputed_theme_state_daily(self, **kwargs: Any) -> SectorPrecomputedThemeStateDailyResponse:
        return self.get_theme_state_daily(**kwargs)

    def get_precomputed_sector_alpha_factors_daily(
        self,
        *,
        trade_date: str | None = None,
        factor_rule: str | None = None,
        **kwargs: Any,
    ) -> SectorPrecomputedSectorAlphaFactorsDailyResponse:
        if trade_date is not None:
            kwargs.update(start_date=trade_date, end_date=trade_date)
        return self.get_sector_factors_daily(rule=factor_rule, **kwargs)

    def get_precomputed_ticker_alpha_factors_daily(
        self,
        *,
        trade_date: str | None = None,
        factor_rule: str | None = None,
        **kwargs: Any,
    ) -> SectorPrecomputedTickerAlphaFactorsDailyResponse:
        if trade_date is not None:
            kwargs.update(start_date=trade_date, end_date=trade_date)
        return self.get_ticker_factors_daily(rule=factor_rule, **kwargs)

    def get_precomputed_manifest(self) -> Any:
        """Retrieves statically precomputed manifest metadata."""
        return self._get("/api/qdata/v1/sector/precomputed/manifest", cast_to=None)


class AsyncSectors(AsyncAPIResource):

    async def get(self) -> SectorsResponse:
        """Retrieves list of all sectors asynchronously.

        Returns
        -------
        SectorsResponse
            The list of sectors.
        """
        return await self._get("/api/qdata/v1/sectors", cast_to=SectorsResponse)

    async def get_metrics(
        self,
        *,
        metric_type: str,
        page: int | None = None,
        size: int | None = None,
        limit: int | None = None,
        order_by: str | None = None,
        order_type: str | None = None,
        include_fields: List[str] | None = None,
        sector: str | None = None,
        as_of_date: str | None = None,
    ) -> SectorMetricsResponse:
        """Retrieves performance metrics for sectors asynchronously.

        Parameters
        ----------
        metric_type : str
            The type of metric to retrieve.
        page : int, optional
            Page number for pagination.
        size : int, optional
            Number of elements per page.
        limit : int, optional
            Max number of records to return.
        order_by : str, optional
            Field name to sort results by.
        order_type : str, optional
            Sort direction (asc or desc).
        include_fields : list of str, optional
            Specific fields to include in the response.
        sector : str, optional
            Specific sector name to filter by.
        as_of_date : str, optional
            Filter records as of a specific date (e.g. 2026-05-28).
        """
        params: dict[str, Any] = {"metric_type": metric_type}
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
        if sector is not None:
            params["sector"] = sector
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return await self._get(
            "/api/qdata/v1/sectors/metrics",
            cast_to=SectorMetricsResponse,
            options={"params": params},
        )

    async def get_info(
        self,
        *,
        name: str | None = None,
        name_alias: str | None = None,
        description_alias: str | None = None,
        level: int | None = None,
        parent_id: int | None = None,
        sensitivity: str | None = None,
        tree: bool | None = None,
    ) -> SectorInfoListResponse:
        """Retrieves detailed sector taxonomy information asynchronously.

        Parameters
        ----------
        name : str, optional
            Sector name.
        name_alias : str, optional
            Sector name alias.
        description_alias : str, optional
            Sector description alias.
        level : int, optional
            Sector hierarchy level.
        parent_id : int, optional
            Parent sector ID.
        sensitivity : str, optional
            Sector sensitivity.
        tree : bool, optional
            Whether to return in tree format (default: False).
        """
        params: dict[str, Any] = {}
        if name is not None:
            params["name"] = name
        if name_alias is not None:
            params["name_alias"] = name_alias
        if description_alias is not None:
            params["description_alias"] = description_alias
        if level is not None:
            params["level"] = level
        if parent_id is not None:
            params["parent_id"] = parent_id
        if sensitivity is not None:
            params["sensitivity"] = sensitivity
        if tree is not None:
            params["tree"] = tree
        return await self._get(
            "/api/qdata/v1/sector/info",
            cast_to=SectorInfoListResponse,
            options={"params": params},
        )

    info = get_info

    async def create_info(self, *, body: dict[str, Any]) -> SectorInfoCreateResponse:
        """Creates new sector taxonomy items asynchronously.

        Parameters
        ----------
        body : dict
            Request body containing items to create.
        """
        return await self._post(
            "/api/qdata/v1/sector/info",
            cast_to=SectorInfoCreateResponse,
            options={"json": body},
        )

    async def get_symbol_relations(
        self,
        *,
        sector_name: str | None = None,
        symbol: str | None = None,
        relation_priority: str | None = None,
        market: str | None = None,
    ) -> SectorSymbolRelationListResponse:
        """Retrieves relationships between sectors and stock/instrument symbols asynchronously.

        Parameters
        ----------
        sector_name : str, optional
            Sector name to query.
        symbol : str, optional
            Symbol to query.
        relation_priority : str, optional
            Relation priority filter.
        """
        params: dict[str, Any] = {}
        if sector_name is not None:
            params["sector_name"] = sector_name
        if symbol is not None:
            params["symbol"] = symbol
        if relation_priority is not None:
            params["relation_priority"] = relation_priority
        if market is not None:
            params["market"] = market
        return await self._get(
            "/api/qdata/v1/sector/symbol_relations",
            cast_to=SectorSymbolRelationListResponse,
            options={"params": params},
        )

    symbol_relations = get_symbol_relations

    async def create_symbol_relations(self, *, body: dict[str, Any]) -> SectorSymbolRelationCreateResponse:
        """Maps symbols to sectors asynchronously.

        Parameters
        ----------
        body : dict
            Request body containing symbol mappings.
        """
        return await self._post(
            "/api/qdata/v1/sector/symbol_relations",
            cast_to=SectorSymbolRelationCreateResponse,
            options={"json": body},
        )

    async def get_movers(
        self,
        *,
        market: str | None = None,
        scope: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> SectorMoversResponse:
        return await self._get(
            "/api/qdata/v1/sector/movers",
            cast_to=SectorMoversResponse,
            options={"params": _params(market=market, scope=scope, start_date=start_date, end_date=end_date)},
        )

    async def get_constituents(
        self,
        *,
        market: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedConstituentsResponse:
        path = "/api/qdata/v1/market/sectors/constituents" if self._client.online else "/api/qdata/v1/sector/precomputed/constituents"
        return await self._get(
            path,
            cast_to=SectorPrecomputedConstituentsResponse,
            options={
                "params": _params(
                    market=market,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    async def get_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedDailyResponse:
        path = "/api/qdata/v1/market/sectors/daily" if self._client.online else "/api/qdata/v1/sector/precomputed/sector_daily"
        return await self._get(
            path,
            cast_to=SectorPrecomputedDailyResponse,
            options={
                "params": _daily_params(
                    market=market,
                    start_date=start_date,
                    end_date=end_date,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    benchmark_id=benchmark_id,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    async def get_ticker_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedTickerDailyResponse:
        path = "/api/qdata/v1/market/tickers/daily" if self._client.online else "/api/qdata/v1/sector/precomputed/ticker_daily"
        return await self._get(
            path,
            cast_to=SectorPrecomputedTickerDailyResponse,
            options={
                "params": _daily_params(
                    market=market,
                    start_date=start_date,
                    end_date=end_date,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    ticker=ticker,
                    role=role,
                    benchmark_id=benchmark_id,
                    limit=limit,
                    offset=offset,
                )
            },
        )

    async def get_fundamentals_periods(
        self,
        *,
        market: str,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        report_period_key: str | None = None,
        limit: int | None = None,
    ) -> SectorPrecomputedFundamentalsPeriodResponse:
        return await self._get(
            "/api/qdata/v1/market/sectors/fundamentals/periods",
            cast_to=SectorPrecomputedFundamentalsPeriodResponse,
            options={
                "params": _params(
                    market=market,
                    scope=scope,
                    level1_id=level1_id,
                    level2_id=level2_id,
                    level3_id=level3_id,
                    report_period_key=report_period_key,
                    limit=limit,
                )
            },
        )

    async def get_horizon_metrics_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedSectorHorizonMetricsResponse:
        params = _daily_params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return await self._get(
            "/api/qdata/v1/market/sectors/horizon-metrics/daily",
            cast_to=SectorPrecomputedSectorHorizonMetricsResponse,
            options={"params": params},
        )

    async def get_theme_state_daily(
        self,
        *,
        market: str,
        start_date: str | None = None,
        end_date: str | None = None,
        scope: str | None = None,
        level1_id: int | None = None,
        level2_id: int | None = None,
        level3_id: int | None = None,
        ticker: str | None = None,
        role: str | None = None,
        benchmark_id: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> SectorPrecomputedThemeStateDailyResponse:
        params = _daily_params(
            market=market,
            start_date=start_date,
            end_date=end_date,
            scope=scope,
            level1_id=level1_id,
            level2_id=level2_id,
            level3_id=level3_id,
            ticker=ticker,
            role=role,
            benchmark_id=benchmark_id,
            limit=limit,
            offset=offset,
        )
        return await self._get(
            "/api/qdata/v1/market/sectors/theme-state/daily",
            cast_to=SectorPrecomputedThemeStateDailyResponse,
            options={"params": params},
        )

    async def get_sector_factors_daily(
        self,
        *,
        market: str,
        level3_id: int,
        rule: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        latest: bool | None = None,
    ) -> SectorPrecomputedSectorAlphaFactorsDailyResponse:
        return await self._get(
            "/api/qdata/v1/market/sectors/factors/daily",
            cast_to=SectorPrecomputedSectorAlphaFactorsDailyResponse,
            options={
                "params": _params(
                    market=market,
                    level3_id=level3_id,
                    rule=rule,
                    start_date=start_date,
                    end_date=end_date,
                    latest=latest,
                )
            },
        )

    async def get_ticker_factors_daily(
        self,
        *,
        market: str,
        ticker: str,
        rule: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        latest: bool | None = None,
    ) -> SectorPrecomputedTickerAlphaFactorsDailyResponse:
        return await self._get(
            "/api/qdata/v1/market/tickers/factors/daily",
            cast_to=SectorPrecomputedTickerAlphaFactorsDailyResponse,
            options={
                "params": _params(
                    market=market,
                    ticker=ticker,
                    rule=rule,
                    start_date=start_date,
                    end_date=end_date,
                    latest=latest,
                )
            },
        )

    async def get_precomputed_constituents(self, **kwargs: Any) -> SectorPrecomputedConstituentsResponse:
        return await self.get_constituents(**kwargs)

    async def get_precomputed_sector_daily(self, **kwargs: Any) -> SectorPrecomputedDailyResponse:
        return await self.get_daily(**kwargs)

    async def get_precomputed_ticker_daily(self, **kwargs: Any) -> SectorPrecomputedTickerDailyResponse:
        return await self.get_ticker_daily(**kwargs)

    async def get_precomputed_fundamentals_period(self, **kwargs: Any) -> SectorPrecomputedFundamentalsPeriodResponse:
        return await self.get_fundamentals_periods(**kwargs)

    async def get_precomputed_market_benchmark_daily(self, **kwargs: Any) -> SectorPrecomputedMarketBenchmarkDailyResponse:
        return await self._client.benchmark.get_market_daily(**kwargs)

    async def get_precomputed_sector_horizon_metrics(self, **kwargs: Any) -> SectorPrecomputedSectorHorizonMetricsResponse:
        return await self.get_horizon_metrics_daily(**kwargs)

    async def get_precomputed_theme_state_daily(self, **kwargs: Any) -> SectorPrecomputedThemeStateDailyResponse:
        return await self.get_theme_state_daily(**kwargs)

    async def get_precomputed_sector_alpha_factors_daily(
        self,
        *,
        trade_date: str | None = None,
        factor_rule: str | None = None,
        **kwargs: Any,
    ) -> SectorPrecomputedSectorAlphaFactorsDailyResponse:
        if trade_date is not None:
            kwargs.update(start_date=trade_date, end_date=trade_date)
        return await self.get_sector_factors_daily(rule=factor_rule, **kwargs)

    async def get_precomputed_ticker_alpha_factors_daily(
        self,
        *,
        trade_date: str | None = None,
        factor_rule: str | None = None,
        **kwargs: Any,
    ) -> SectorPrecomputedTickerAlphaFactorsDailyResponse:
        if trade_date is not None:
            kwargs.update(start_date=trade_date, end_date=trade_date)
        return await self.get_ticker_factors_daily(rule=factor_rule, **kwargs)

    async def get_precomputed_manifest(self) -> Any:
        """Retrieves statically precomputed manifest metadata asynchronously."""
        return await self._get("/api/qdata/v1/sector/precomputed/manifest", cast_to=None)
