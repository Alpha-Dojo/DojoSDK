from __future__ import annotations

from typing import Any, List
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    SectorsResponse,
    SectorMetricsResponse,
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
