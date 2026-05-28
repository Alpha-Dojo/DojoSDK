from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import CacheResponse


class Cache(SyncAPIResource):

    def clear(self, *, exchange: str | None = None) -> CacheResponse:
        """Clears the market data cache reset for the given exchange.

        Parameters
        ----------
        exchange : str, optional
            The name of the exchange to clear cache for (e.g. BINANCE). If omitted, clears all cache.
        """
        params: dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        return self._delete("/api/qdata/v1/cache", cast_to=CacheResponse, options={"params": params})


class AsyncCache(AsyncAPIResource):

    async def clear(self, *, exchange: str | None = None) -> CacheResponse:
        """Clears the market data cache reset for the given exchange asynchronously.

        Parameters
        ----------
        exchange : str, optional
            The name of the exchange to clear cache for (e.g. BINANCE). If omitted, clears all cache.
        """
        params: dict[str, Any] = {}
        if exchange is not None:
            params["exchange"] = exchange
        return await self._delete("/api/qdata/v1/cache", cast_to=CacheResponse, options={"params": params})
