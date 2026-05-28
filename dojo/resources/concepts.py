from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    ConceptInfoResponse,
    ConceptConstituentsResponse,
    ConceptQuoteResponse,
)


class Concepts(SyncAPIResource):

    def get_info(self, *, source: str | None = None, market: str | None = None) -> ConceptInfoResponse:
        """Retrieves general concept lists and information.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        return self._get("/api/qdata/v1/concepts", cast_to=ConceptInfoResponse, options={"params": params})

    def get_constituents(
        self,
        *,
        source: str | None = None,
        market: str | None = None,
        concept_id: str | None = None,
    ) -> ConceptConstituentsResponse:
        """Retrieves constituents of a specific concept.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        concept_id : str, optional
            The identifier of the concept theme.
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        if concept_id is not None:
            params["concept_id"] = concept_id
        return self._get("/api/qdata/v1/concepts/constituents", cast_to=ConceptConstituentsResponse, options={"params": params})

    def get_quote(
        self,
        *,
        source: str | None = None,
        market: str | None = None,
        return_tickers: bool | None = None,
    ) -> ConceptQuoteResponse:
        """Retrieves pricing/quote data for concepts.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        return_tickers : bool, optional
            Whether to include tickers inside the returned concept structure.
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        if return_tickers is not None:
            params["return_tickers"] = return_tickers
        return self._get("/api/qdata/v1/concepts/quote", cast_to=ConceptQuoteResponse, options={"params": params})


class AsyncConcepts(AsyncAPIResource):

    async def get_info(self, *, source: str | None = None, market: str | None = None) -> ConceptInfoResponse:
        """Retrieves general concept lists and information asynchronously.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        return await self._get("/api/qdata/v1/concepts", cast_to=ConceptInfoResponse, options={"params": params})

    async def get_constituents(
        self,
        *,
        source: str | None = None,
        market: str | None = None,
        concept_id: str | None = None,
    ) -> ConceptConstituentsResponse:
        """Retrieves constituents of a specific concept asynchronously.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        concept_id : str, optional
            The identifier of the concept theme.
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        if concept_id is not None:
            params["concept_id"] = concept_id
        return await self._get("/api/qdata/v1/concepts/constituents", cast_to=ConceptConstituentsResponse, options={"params": params})

    async def get_quote(
        self,
        *,
        source: str | None = None,
        market: str | None = None,
        return_tickers: bool | None = None,
    ) -> ConceptQuoteResponse:
        """Retrieves pricing/quote data for concepts asynchronously.

        Parameters
        ----------
        source : str, optional
            Source provider of the concepts.
        market : str, optional
            Market segment (e.g. US, CN, Crypto).
        return_tickers : bool, optional
            Whether to include tickers inside the returned concept structure.
        """
        params: dict[str, Any] = {}
        if source is not None:
            params["source"] = source
        if market is not None:
            params["market"] = market
        if return_tickers is not None:
            params["return_tickers"] = return_tickers
        return await self._get("/api/qdata/v1/concepts/quote", cast_to=ConceptQuoteResponse, options={"params": params})
