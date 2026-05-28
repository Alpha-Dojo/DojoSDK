from __future__ import annotations

from typing import Any
from dojo.resources.base import SyncAPIResource, AsyncAPIResource
from dojo.types.models import (
    UserTraitsResponse,
    UserAnalyticsResponse,
)


# --- Sync User Sub-resources ---
class UserTraits(SyncAPIResource):

    def get(
        self,
        *,
        user_id: str,
        region: str | None = None,
        last_active_time: str | None = None,
        as_of_date: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> UserTraitsResponse:
        """Retrieves traits for a user.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user.
        region : str, optional
            Regional filter.
        last_active_time : str, optional
            ISO-8601 timestamp of last activity.
        as_of_date : str, optional
            Evaluation reference date.
        body : dict, optional
            Optional request body payload.
        """
        params: dict[str, Any] = {"user_id": user_id}
        if region is not None:
            params["region"] = region
        if last_active_time is not None:
            params["last_active_time"] = last_active_time
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return self._get("/api/qdata/v1/user/traits", cast_to=UserTraitsResponse, options={"params": params, "json": body})

    def update(self, *, body: dict[str, Any]) -> UserTraitsResponse:
        """Saves or updates user traits.

        Parameters
        ----------
        body : dict
            A dictionary containing traits data to update.
        """
        return self._put("/api/qdata/v1/user/traits", cast_to=UserTraitsResponse, options={"json": body})

    def get_by_id(
        self,
        *,
        user_id: str,
        region: str | None = None,
        last_active_time: str | None = None,
        as_of_date: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> UserTraitsResponse:
        """Retrieves traits for a specific user ID via path parameter.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user in path.
        region : str, optional
            Regional filter.
        last_active_time : str, optional
            ISO-8601 timestamp of last activity.
        as_of_date : str, optional
            Evaluation reference date.
        body : dict, optional
            Optional request body payload.
        """
        params: dict[str, Any] = {}
        if region is not None:
            params["region"] = region
        if last_active_time is not None:
            params["last_active_time"] = last_active_time
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return self._get(f"/api/qdata/v1/user/traits/{user_id}", cast_to=UserTraitsResponse, options={"params": params, "json": body})

    def update_by_id(self, *, user_id: str, body: dict[str, Any]) -> UserTraitsResponse:
        """Updates user traits for a specific user ID via path parameter.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user.
        body : dict
            A dictionary containing traits data to update.
        """
        return self._put(f"/api/qdata/v1/user/traits/{user_id}", cast_to=UserTraitsResponse, options={"json": body})


class UserAnalytics(SyncAPIResource):

    def upload(self, *, body: dict[str, Any]) -> UserAnalyticsResponse:
        """Uploads analytics tracking data for user behaviors.

        Parameters
        ----------
        body : dict
            A dictionary containing behavioral analytics tracking details.
        """
        return self._put("/api/qdata/v1/user/analytics", cast_to=UserAnalyticsResponse, options={"json": body})


class User(SyncAPIResource):

    def __init__(self, client: Any, is_raw: bool = False) -> None:
        super().__init__(client, is_raw=is_raw)
        self.traits = UserTraits(client, is_raw=is_raw)
        self.analytics = UserAnalytics(client, is_raw=is_raw)


# --- Async User Sub-resources ---
class AsyncUserTraits(AsyncAPIResource):

    async def get(
        self,
        *,
        user_id: str,
        region: str | None = None,
        last_active_time: str | None = None,
        as_of_date: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> UserTraitsResponse:
        """Retrieves traits for a user asynchronously.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user.
        region : str, optional
            Regional filter.
        last_active_time : str, optional
            ISO-8601 timestamp of last activity.
        as_of_date : str, optional
            Evaluation reference date.
        body : dict, optional
            Optional request body payload.
        """
        params: dict[str, Any] = {"user_id": user_id}
        if region is not None:
            params["region"] = region
        if last_active_time is not None:
            params["last_active_time"] = last_active_time
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return await self._get("/api/qdata/v1/user/traits", cast_to=UserTraitsResponse, options={"params": params, "json": body})

    async def update(self, *, body: dict[str, Any]) -> UserTraitsResponse:
        """Saves or updates user traits asynchronously.

        Parameters
        ----------
        body : dict
            A dictionary containing traits data to update.
        """
        return await self._put("/api/qdata/v1/user/traits", cast_to=UserTraitsResponse, options={"json": body})

    async def get_by_id(
        self,
        *,
        user_id: str,
        region: str | None = None,
        last_active_time: str | None = None,
        as_of_date: str | None = None,
        body: dict[str, Any] | None = None,
    ) -> UserTraitsResponse:
        """Retrieves traits for a specific user ID asynchronously.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user in path.
        region : str, optional
            Regional filter.
        last_active_time : str, optional
            ISO-8601 timestamp of last activity.
        as_of_date : str, optional
            Evaluation reference date.
        body : dict, optional
            Optional request body payload.
        """
        params: dict[str, Any] = {}
        if region is not None:
            params["region"] = region
        if last_active_time is not None:
            params["last_active_time"] = last_active_time
        if as_of_date is not None:
            params["as_of_date"] = as_of_date
        return await self._get(f"/api/qdata/v1/user/traits/{user_id}", cast_to=UserTraitsResponse, options={"params": params, "json": body})

    async def update_by_id(self, *, user_id: str, body: dict[str, Any]) -> UserTraitsResponse:
        """Updates user traits for a specific user ID asynchronously.

        Parameters
        ----------
        user_id : str
            Unique identifier of the target user.
        body : dict
            A dictionary containing traits data to update.
        """
        return await self._put(f"/api/qdata/v1/user/traits/{user_id}", cast_to=UserTraitsResponse, options={"json": body})


class AsyncUserAnalytics(AsyncAPIResource):

    async def upload(self, *, body: dict[str, Any]) -> UserAnalyticsResponse:
        """Uploads analytics tracking data asynchronously.

        Parameters
        ----------
        body : dict
            A dictionary containing behavioral analytics tracking details.
        """
        return await self._put("/api/qdata/v1/user/analytics", cast_to=UserAnalyticsResponse, options={"json": body})


class AsyncUser(AsyncAPIResource):

    def __init__(self, client: Any, is_raw: bool = False) -> None:
        super().__init__(client, is_raw=is_raw)
        self.traits = AsyncUserTraits(client, is_raw=is_raw)
        self.analytics = AsyncUserAnalytics(client, is_raw=is_raw)
