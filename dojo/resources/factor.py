from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List

from dojo._compat import model_dump, model_validate
from dojo.resources.base import AsyncAPIResource, SyncAPIResource
from dojo.types.models import (
    FactorQueryRequest,
    FactorQueryResponse,
    FactorTablesResponse,
    OrderBySpec,
)


def _build_factor_query_payload(
    *,
    body: FactorQueryRequest | dict[str, Any] | None = None,
    table_name: str | None = None,
    start_date: date | datetime | str | None = None,
    end_date: date | datetime | str | None = None,
    tickers: List[str] | str | None = None,
    listing_market: str | List[str] | None = None,
    filters: Dict[str, Any] | None = None,
    fields: List[str] | None = None,
    order_by: List[str | OrderBySpec | Dict[str, Any]] | str | None = None,
    page: int | None = None,
    size: int | None = None,
    include_total: bool | None = None,
) -> dict[str, Any]:
    explicit_kwargs = {
        key: value
        for key, value in {
            "table_name": table_name,
            "start_date": start_date,
            "end_date": end_date,
            "tickers": tickers,
            "listing_market": listing_market,
            "filters": filters,
            "fields": fields,
            "order_by": order_by,
            "page": page,
            "size": size,
            "include_total": include_total,
        }.items()
        if value is not None
    }

    if body is not None:
        if isinstance(body, FactorQueryRequest):
            raw_data = model_dump(body, mode="json", exclude_unset=True)
        elif isinstance(body, dict):
            raw_data = dict(body)
        else:
            raise TypeError("body must be a FactorQueryRequest or dict")
        raw_data.update(explicit_kwargs)
        request = model_validate(FactorQueryRequest, raw_data)
    else:
        request = model_validate(FactorQueryRequest, explicit_kwargs)

    payload = model_dump(request, mode="json", exclude_none=True)
    if "order_by" in payload and isinstance(payload["order_by"], list):
        payload["order_by"] = [model_dump(item, mode="json", exclude_none=True) if isinstance(item, OrderBySpec) else item for item in payload["order_by"]]
    return payload


def _build_factor_tables_params(
    *,
    table_name: str | None = None,
    include_columns: bool | None = None,
    refresh_schema: bool | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if table_name is not None:
        params["table_name"] = table_name
    if include_columns is not None:
        params["include_columns"] = include_columns
    if refresh_schema is not None:
        params["refresh_schema"] = refresh_schema
    return params


class Factor(SyncAPIResource):
    """Synchronous Factor API resource for querying factor tables and schemas."""

    def query(
        self,
        *,
        body: FactorQueryRequest | dict[str, Any] | None = None,
        table_name: str | None = None,
        start_date: date | datetime | str | None = None,
        end_date: date | datetime | str | None = None,
        tickers: List[str] | str | None = None,
        listing_market: str | List[str] | None = None,
        filters: Dict[str, Any] | None = None,
        fields: List[str] | None = None,
        order_by: List[str | OrderBySpec | Dict[str, Any]] | str | None = None,
        page: int | None = None,
        size: int | None = None,
        include_total: bool | None = None,
    ) -> FactorQueryResponse:
        """Generic query endpoint for factor tables in DuckDB S3 Tables (Iceberg).

        Supports table selection (`table_name`), date/time range (`start_date`, `end_date`),
        symbol/market shortcuts (`tickers`, `listing_market`), generic column `filters`,
        column projection (`fields`), deterministic multi-column `order_by`, and pagination
        (`page`, `size`, `include_total`).

        Parameters
        ----------
        body : FactorQueryRequest or dict, optional
            Complete request payload. Any explicitly provided keyword arguments will
            override the corresponding fields in `body`.
        table_name : str, optional
            Registered factor table name in S3 Tables (defaults to 'etf_daily_factors').
        start_date : date, datetime, or str, optional
            Inclusive lower bound on the table's time column (YYYY-MM-DD or ISO datetime).
        end_date : date, datetime, or str, optional
            Inclusive upper bound on the table's time column (YYYY-MM-DD or ISO datetime).
        tickers : list of str or str, optional
            Optional symbol/ticker filter (list of tickers or comma-separated string, max 500).
        listing_market : str or list of str, optional
            Optional market filter mapped to the table's market column (e.g. 'US' or ['US', 'HK']).
        filters : dict, optional
            Generic column filters. Supports shorthand `{'col': val_or_list}` and operator
            dicts `{'col': {'eq'|'ne'|'gt'|'gte'|'lt'|'lte'|'in'|'not_in'|'is_null': val}}`.
        fields : list of str, optional
            Optional list of columns to return. Omit or pass None to return all columns.
        order_by : list of str/OrderBySpec/dict or str, optional
            Optional sort rules, e.g. `['as_of_date desc', 'ticker asc']` or
            `[{'field': 'as_of_date', 'direction': 'desc'}]`.
        page : int, optional
            1-based page number (1 to 1000, default 1).
        size : int, optional
            Page size (1 to 1000, default 100).
        include_total : bool, optional
            Whether to execute COUNT(*) to populate total_num and total_page (default False).
        """
        payload = _build_factor_query_payload(
            body=body,
            table_name=table_name,
            start_date=start_date,
            end_date=end_date,
            tickers=tickers,
            listing_market=listing_market,
            filters=filters,
            fields=fields,
            order_by=order_by,
            page=page,
            size=size,
            include_total=include_total,
        )
        return self._post(
            "/api/qdata/v1/factor/query",
            cast_to=FactorQueryResponse,
            options={"json": payload},
        )

    def get_tables(
        self,
        *,
        table_name: str | None = None,
        include_columns: bool | None = None,
        refresh_schema: bool | None = None,
    ) -> FactorTablesResponse:
        """List registered factor tables and their dynamically discovered column schemas.

        Parameters
        ----------
        table_name : str, optional
            Filter by a specific registered factor table name.
        include_columns : bool, optional
            Whether to include dynamically discovered column schemas (server default True).
        refresh_schema : bool, optional
            Whether to force refresh the table schema cache (server default False).
        """
        params = _build_factor_tables_params(
            table_name=table_name,
            include_columns=include_columns,
            refresh_schema=refresh_schema,
        )
        return self._get(
            "/api/qdata/v1/factor/tables",
            cast_to=FactorTablesResponse,
            options={"params": params},
        )

    tables = get_tables


class AsyncFactor(AsyncAPIResource):
    """Asynchronous Factor API resource for querying factor tables and schemas."""

    async def query(
        self,
        *,
        body: FactorQueryRequest | dict[str, Any] | None = None,
        table_name: str | None = None,
        start_date: date | datetime | str | None = None,
        end_date: date | datetime | str | None = None,
        tickers: List[str] | str | None = None,
        listing_market: str | List[str] | None = None,
        filters: Dict[str, Any] | None = None,
        fields: List[str] | None = None,
        order_by: List[str | OrderBySpec | Dict[str, Any]] | str | None = None,
        page: int | None = None,
        size: int | None = None,
        include_total: bool | None = None,
    ) -> FactorQueryResponse:
        """Generic query endpoint for factor tables in DuckDB S3 Tables (Iceberg) asynchronously.

        See :meth:`Factor.query` for parameter details.
        """
        payload = _build_factor_query_payload(
            body=body,
            table_name=table_name,
            start_date=start_date,
            end_date=end_date,
            tickers=tickers,
            listing_market=listing_market,
            filters=filters,
            fields=fields,
            order_by=order_by,
            page=page,
            size=size,
            include_total=include_total,
        )
        return await self._post(
            "/api/qdata/v1/factor/query",
            cast_to=FactorQueryResponse,
            options={"json": payload},
        )

    async def get_tables(
        self,
        *,
        table_name: str | None = None,
        include_columns: bool | None = None,
        refresh_schema: bool | None = None,
    ) -> FactorTablesResponse:
        """List registered factor tables and their dynamically discovered column schemas asynchronously.

        See :meth:`Factor.get_tables` for parameter details.
        """
        params = _build_factor_tables_params(
            table_name=table_name,
            include_columns=include_columns,
            refresh_schema=refresh_schema,
        )
        return await self._get(
            "/api/qdata/v1/factor/tables",
            cast_to=FactorTablesResponse,
            options={"params": params},
        )

    tables = get_tables
