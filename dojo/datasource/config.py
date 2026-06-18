from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


@dataclass
class HFConfig:
    """HuggingFace offline datasource config from environment variables."""

    token: str | None = None
    revision: str = "main"
    cache_dir: str = os.path.expanduser("~/.cache/dojo")
    local_only: bool = False
    repo_prefix: str = "flowhale"

    @classmethod
    def from_env(cls) -> "HFConfig":
        return cls(
            token=os.environ.get("DOJO_HF_TOKEN"),
            revision=os.environ.get("DOJO_HF_REVISION", "main"),
            cache_dir=os.environ.get("DOJO_CACHE_DIR", os.path.expanduser("~/.cache/dojo")),
            local_only=_env_bool("DOJO_HF_OFFLINE", False),
            repo_prefix=os.environ.get("DOJO_HF_REPO_PREFIX", "flowhale"),
        )


def is_online() -> bool:
    """Global switch: True (online) by default."""
    return _env_bool("DOJO_ONLINE", True)
