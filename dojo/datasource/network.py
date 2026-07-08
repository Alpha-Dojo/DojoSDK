from __future__ import annotations

import urllib.request
import urllib.error
import socket
from dojo.datasource.config import HFConfig
from dojo.logging import logger

_cached_is_in_mainland_china: bool | None = None


def is_in_mainland_china() -> bool:
    """
    Detects if the current network is in Mainland China by attempting an HTTPS
    connection to google.com. Due to SNI blocking, this will reliably and quickly
    fail (timeout or connection reset) in Mainland China.
    """
    global _cached_is_in_mainland_china
    if _cached_is_in_mainland_china is not None:
        return _cached_is_in_mainland_china

    try:
        # Use a short timeout. 3 seconds is usually enough to establish a TLS handshake.
        urllib.request.urlopen("https://www.google.com", timeout=3.0)
        _cached_is_in_mainland_china = False
    except (urllib.error.URLError, socket.timeout, ConnectionError):
        _cached_is_in_mainland_china = True
    except Exception as e:
        logger.debug(f"Unexpected error during network detection: {e}")
        _cached_is_in_mainland_china = True

    return _cached_is_in_mainland_china


def resolve_backend(config: HFConfig) -> str:
    """
    Resolves the data backend ('modelscope' or 'huggingface') based on configuration
    and network conditions.
    """
    if config.backend in ("modelscope", "huggingface"):
        return config.backend

    if is_in_mainland_china():
        return "modelscope"
    return "huggingface"
