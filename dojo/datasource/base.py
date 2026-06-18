from __future__ import annotations

from typing import Any, Protocol


class DataSource(Protocol):
    """Unified data source protocol: resolves a request into an API-equivalent JSON envelope."""

    def fetch(
        self,
        *,
        method: str,
        path: str,
        params: dict[str, Any],
        json: Any | None = None,
    ) -> Any:
        """Returns a dictionary shaped like {"code":0, "data":[...]}, or bare list/dict."""
        ...
