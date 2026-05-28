from __future__ import annotations

from typing import Any


class SyncAPIResource:
    def __init__(self, client: Any, is_raw: bool = False) -> None:
        self._client = client
        self._is_raw = is_raw

        if is_raw:
            self._get = lambda path, cast_to, options=None: client.get(path, cast_to=cast_to, options=self._add_raw(options))
            self._post = lambda path, cast_to, options=None: client.post(path, cast_to=cast_to, options=self._add_raw(options))
            self._put = lambda path, cast_to, options=None: client.put(path, cast_to=cast_to, options=self._add_raw(options))
            self._delete = lambda path, cast_to, options=None: client.delete(path, cast_to=cast_to, options=self._add_raw(options))
        else:
            self._get = client.get
            self._post = client.post
            self._put = client.put
            self._delete = client.delete

    def _add_raw(self, options: dict[str, Any] | None) -> dict[str, Any]:
        opts = dict(options) if options is not None else {}
        opts["is_raw"] = True
        return opts

    @property
    def with_raw_response(self) -> Any:
        return self.__class__(self._client, is_raw=True)


class AsyncAPIResource:
    def __init__(self, client: Any, is_raw: bool = False) -> None:
        self._client = client
        self._is_raw = is_raw

        if is_raw:
            self._get = lambda path, cast_to, options=None: client.get(path, cast_to=cast_to, options=self._add_raw(options))
            self._post = lambda path, cast_to, options=None: client.post(path, cast_to=cast_to, options=self._add_raw(options))
            self._put = lambda path, cast_to, options=None: client.put(path, cast_to=cast_to, options=self._add_raw(options))
            self._delete = lambda path, cast_to, options=None: client.delete(path, cast_to=cast_to, options=self._add_raw(options))
        else:
            self._get = client.get
            self._post = client.post
            self._put = client.put
            self._delete = client.delete

    def _add_raw(self, options: dict[str, Any] | None) -> dict[str, Any]:
        opts = dict(options) if options is not None else {}
        opts["is_raw"] = True
        return opts

    @property
    def with_raw_response(self) -> Any:
        return self.__class__(self._client, is_raw=True)
