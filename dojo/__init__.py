from dojo.client.sync import Dojo as Dojo
from dojo.client.async_client import AsyncDojo as AsyncDojo

import importlib.metadata

try:
    __version__ = importlib.metadata.version("dojosdk")
except importlib.metadata.PackageNotFoundError:
    __version__ = "unknown"


from dojo._exceptions import (
    DojoError as DojoError,
    APIError as APIError,
    APIConnectionError as APIConnectionError,
    APITimeoutError as APITimeoutError,
    APIResponseValidationError as APIResponseValidationError,
    APIStatusError as APIStatusError,
    BadRequestError as BadRequestError,
    AuthenticationError as AuthenticationError,
    PermissionDeniedError as PermissionDeniedError,
    NotFoundError as NotFoundError,
    ConflictError as ConflictError,
    UnprocessableEntityError as UnprocessableEntityError,
    RateLimitError as RateLimitError,
    InternalServerError as InternalServerError,
)

__all__ = [
    "__version__",
    "Dojo",
    "AsyncDojo",
    "DojoError",
    "APIError",
    "APIConnectionError",
    "APITimeoutError",
    "APIResponseValidationError",
    "APIStatusError",
    "BadRequestError",
    "AuthenticationError",
    "PermissionDeniedError",
    "NotFoundError",
    "ConflictError",
    "UnprocessableEntityError",
    "RateLimitError",
    "InternalServerError",
]
