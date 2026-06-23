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
    SectorPrecomputedManifestResponse,
    SectorPrecomputedTickerDailyResponse,
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
        return self._get("/api/qdata/v1/sectors/metrics", cast_to=SectorMetricsResponse, options={"params": params})

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
        return self._get("/api/qdata/v1/sector/info", cast_to=SectorInfoListResponse, options={"params": params})

    info = get_info

    def create_info(self, *, body: dict[str, Any]) -> SectorInfoCreateResponse:
        """Creates new sector taxonomy items.

        Parameters
        ----------
        body : dict
            Request body containing items to create.
        """
        return self._post("/api/qdata/v1/sector/info", cast_to=SectorInfoCreateResponse, options={"json": body})

    def get_symbol_relations(
        self,
        *,
        sector_name: str | None = None,
        symbol: str | None = None,
        relation_priority: str | None = None,
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
        return self._get("/api/qdata/v1/sector/symbol_relations", cast_to=SectorSymbolRelationListResponse, options={"params": params})

    def create_symbol_relations(self, *, body: dict[str, Any]) -> SectorSymbolRelationCreateResponse:
        """Maps symbols to sectors.

        Parameters
        ----------
        body : dict
            Request body containing symbol mappings.
        """
        return self._post("/api/qdata/v1/sector/symbol_relations", cast_to=SectorSymbolRelationCreateResponse, options={"json": body})

    def get_precomputed_constituents(self) -> SectorPrecomputedConstituentsResponse:
        """Retrieves statically precomputed sector constituents."""
        return self._get("/api/qdata/v1/sector/precomputed/constituents", cast_to=SectorPrecomputedConstituentsResponse)

    def get_precomputed_sector_daily(self) -> SectorPrecomputedDailyResponse:
        """Retrieves statically precomputed daily sector performance."""
        return self._get("/api/qdata/v1/sector/precomputed/sector_daily", cast_to=SectorPrecomputedDailyResponse)

    def get_precomputed_ticker_daily(self) -> SectorPrecomputedTickerDailyResponse:
        """Retrieves statically precomputed daily ticker performance."""
        return self._get("/api/qdata/v1/sector/precomputed/ticker_daily", cast_to=SectorPrecomputedTickerDailyResponse)

    def get_precomputed_manifest(self) -> SectorPrecomputedManifestResponse:
        """Retrieves sector precomputed snapshot manifest metadata."""
        return self._get("/api/qdata/v1/sector/precomputed/manifest", cast_to=SectorPrecomputedManifestResponse)


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
        return await self._get("/api/qdata/v1/sectors/metrics", cast_to=SectorMetricsResponse, options={"params": params})

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
        return await self._get("/api/qdata/v1/sector/info", cast_to=SectorInfoListResponse, options={"params": params})

    info = get_info

    async def create_info(self, *, body: dict[str, Any]) -> SectorInfoCreateResponse:
        """Creates new sector taxonomy items asynchronously.

        Parameters
        ----------
        body : dict
            Request body containing items to create.
        """
        return await self._post("/api/qdata/v1/sector/info", cast_to=SectorInfoCreateResponse, options={"json": body})

    async def get_symbol_relations(
        self,
        *,
        sector_name: str | None = None,
        symbol: str | None = None,
        relation_priority: str | None = None,
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
        return await self._get("/api/qdata/v1/sector/symbol_relations", cast_to=SectorSymbolRelationListResponse, options={"params": params})

    symbol_relations = get_symbol_relations

    async def create_symbol_relations(self, *, body: dict[str, Any]) -> SectorSymbolRelationCreateResponse:
        """Maps symbols to sectors asynchronously.

        Parameters
        ----------
        body : dict
            Request body containing symbol mappings.
        """
        return await self._post("/api/qdata/v1/sector/symbol_relations", cast_to=SectorSymbolRelationCreateResponse, options={"json": body})

    async def get_precomputed_constituents(self) -> SectorPrecomputedConstituentsResponse:
        """Retrieves statically precomputed sector constituents asynchronously."""
        return await self._get("/api/qdata/v1/sector/precomputed/constituents", cast_to=SectorPrecomputedConstituentsResponse)

    async def get_precomputed_sector_daily(self) -> SectorPrecomputedDailyResponse:
        """Retrieves statically precomputed daily sector performance asynchronously."""
        return await self._get("/api/qdata/v1/sector/precomputed/sector_daily", cast_to=SectorPrecomputedDailyResponse)

    async def get_precomputed_ticker_daily(self) -> SectorPrecomputedTickerDailyResponse:
        """Retrieves statically precomputed daily ticker performance asynchronously."""
        return await self._get("/api/qdata/v1/sector/precomputed/ticker_daily", cast_to=SectorPrecomputedTickerDailyResponse)

    async def get_precomputed_manifest(self) -> SectorPrecomputedManifestResponse:
        """Retrieves sector precomputed snapshot manifest metadata asynchronously."""
        return await self._get("/api/qdata/v1/sector/precomputed/manifest", cast_to=SectorPrecomputedManifestResponse)
