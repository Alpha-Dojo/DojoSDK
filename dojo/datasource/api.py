from __future__ import annotations

from typing import Any


class ApiDataSource:
    """Online data source wrapper."""

    def __init__(self, client: Any) -> None:
        self._client = client
