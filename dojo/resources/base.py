from __future__ import annotations

from typing import Any
from dojo.logging import logger


class SyncAPIResource:
    def __init__(self, client: Any, is_raw: bool = False) -> None:
        self._client = client
        self._is_raw = is_raw

        self._get = lambda path, cast_to, options=None: self._request("GET", path, cast_to=cast_to, options=options)
        self._post = lambda path, cast_to, options=None: self._request("POST", path, cast_to=cast_to, options=options)
        self._put = lambda path, cast_to, options=None: self._request("PUT", path, cast_to=cast_to, options=options)
        self._delete = lambda path, cast_to, options=None: self._request("DELETE", path, cast_to=cast_to, options=options)

    def _add_raw(self, options: dict[str, Any] | None) -> dict[str, Any]:
        opts = dict(options) if options is not None else {}
        opts["is_raw"] = True
        return opts

    @property
    def with_raw_response(self) -> Any:
        return self.__class__(self._client, is_raw=True)

    def _request(self, method: str, path: str, *, cast_to: Any, options: dict[str, Any] | None = None) -> Any:
        opts = self._add_raw(options) if self._is_raw else (options or {})
        logger.debug(f"Request: {method} {path} | cast_to: {cast_to} | options: {opts}")
        client_func = getattr(self._client, method.lower())
        try:
            return client_func(path, cast_to=cast_to, options=opts)
        except Exception as e:
            err_msg = f"Request error: {method} {path} | Error: {e}"
            if hasattr(e, "body") and getattr(e, "body") is not None:
                err_msg += f" | Body: {getattr(e, 'body')}"
            logger.error(err_msg, exc_info=True)
            raise e


class AsyncAPIResource:
    def __init__(self, client: Any, is_raw: bool = False) -> None:
        self._client = client
        self._is_raw = is_raw

        self._get = lambda path, cast_to, options=None: self._request("GET", path, cast_to=cast_to, options=options)
        self._post = lambda path, cast_to, options=None: self._request("POST", path, cast_to=cast_to, options=options)
        self._put = lambda path, cast_to, options=None: self._request("PUT", path, cast_to=cast_to, options=options)
        self._delete = lambda path, cast_to, options=None: self._request("DELETE", path, cast_to=cast_to, options=options)

    def _add_raw(self, options: dict[str, Any] | None) -> dict[str, Any]:
        opts = dict(options) if options is not None else {}
        opts["is_raw"] = True
        return opts

    @property
    def with_raw_response(self) -> Any:
        return self.__class__(self._client, is_raw=True)

    async def _request(self, method: str, path: str, *, cast_to: Any, options: dict[str, Any] | None = None) -> Any:
        opts = self._add_raw(options) if self._is_raw else (options or {})
        logger.debug(f"Request: {method} {path} | cast_to: {cast_to} | options: {opts}")
        client_func = getattr(self._client, method.lower())
        try:
            return await client_func(path, cast_to=cast_to, options=opts)
        except Exception as e:
            err_msg = f"Request error: {method} {path} | Error: {e}"
            if hasattr(e, "body") and getattr(e, "body") is not None:
                err_msg += f" | Body: {getattr(e, 'body')}"
            logger.error(err_msg, exc_info=True)
            raise e
