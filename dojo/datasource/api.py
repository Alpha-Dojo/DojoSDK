from __future__ import annotations

from typing import Any


class ApiDataSource:
    """Online data source wrapper."""

    def __init__(self, client: Any) -> None:
        self._client = client

    def fetch_df(self, *, path: str, params: dict[str, Any] | None = None) -> Any:
        raise NotImplementedError("fetch_df is currently only supported in Offline huggingface data source.")
