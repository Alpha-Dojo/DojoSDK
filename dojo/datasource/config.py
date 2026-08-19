from __future__ import annotations

import os
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in ("1", "true", "yes", "on")


def _env_float(name: str, default: float) -> float:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = float(raw)
    except ValueError:
        return default
    return value if value > 0 else default


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError:
        return default
    return value if value >= 0 else default


@dataclass
class HFConfig:
    """HuggingFace offline datasource config from environment variables."""

    token: str | None = None
    modelscope_token: str | None = None
    backend: str = "auto"
    revision: str = "main"
    cache_dir: str = os.path.expanduser("~/.cache/huggingface/hub")
    local_only: bool = False
    repo_prefix: str = "flowhale"
    download_timeout_seconds: float = 60.0
    etag_timeout_seconds: float = 10.0
    max_download_retries: int = 1

    @classmethod
    def from_env(cls) -> "HFConfig":
        return cls(
            token=os.environ.get("DOJO_HF_TOKEN"),
            modelscope_token=os.environ.get("DOJO_MODELSCOPE_TOKEN") or os.environ.get("MODELSCOPE_TOKEN"),
            backend=os.environ.get("DOJO_DATA_BACKEND", "auto").lower(),
            revision=os.environ.get("DOJO_HF_REVISION", "main"),
            cache_dir=os.environ.get("DOJO_CACHE_DIR", os.path.expanduser("~/.cache/huggingface/hub")),
            local_only=_env_bool("DOJO_HF_OFFLINE", False),
            repo_prefix=os.environ.get("DOJO_HF_REPO_PREFIX", "flowhale"),
            download_timeout_seconds=_env_float(
                "DOJO_HF_DOWNLOAD_TIMEOUT",
                60.0,
            ),
            etag_timeout_seconds=_env_float(
                "DOJO_HF_ETAG_TIMEOUT",
                10.0,
            ),
            max_download_retries=_env_int(
                "DOJO_HF_MAX_RETRIES",
                1,
            ),
        )


def is_online() -> bool:
    """Global switch: True (online) by default."""
    return _env_bool("DOJO_ONLINE", False)
