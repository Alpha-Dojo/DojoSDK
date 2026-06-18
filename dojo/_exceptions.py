import httpx
from typing import Any


class DojoError(Exception):
    """Base exception for all DojoSDK errors."""

    pass


class APIError(DojoError):
    """Base class for errors related to interacting with the Dojo API."""

    pass


class APIConnectionError(APIError):
    """Raised when the SDK fails to connect to the Dojo API service."""

    def __init__(self, message: str = "Connection error.", *, request: httpx.Request | None = None) -> None:
        super().__init__(message)
        self.request = request


class APITimeoutError(APIConnectionError):
    """Raised when a request to the Dojo API times out."""

    def __init__(self, message: str = "Request timed out.", *, request: httpx.Request | None = None) -> None:
        super().__init__(message, request=request)


class APIResponseValidationError(APIError):
    """Raised when the API response does not conform to the expected Pydantic schema."""

    def __init__(self, response: httpx.Response, body: Any, message: str = "API response did not match expected schema.") -> None:
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.body = body


class APIStatusError(APIError):
    """Raised when the Dojo API returns a non-2xx status code."""

    def __init__(self, message: str, *, response: httpx.Response, body: Any) -> None:
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code
        self.body = body


class BadRequestError(APIStatusError):
    """HTTP 400 Bad Request."""

    pass


class AuthenticationError(APIStatusError):
    """HTTP 401 Unauthorized."""

    pass


class PermissionDeniedError(APIStatusError):
    """HTTP 403 Forbidden."""

    pass


class NotFoundError(APIStatusError):
    """HTTP 404 Not Found."""

    pass


class ConflictError(APIStatusError):
    """HTTP 409 Conflict."""

    pass


class UnprocessableEntityError(APIStatusError):
    """HTTP 422 Unprocessable Entity."""

    pass


class RateLimitError(APIStatusError):
    """HTTP 429 Rate Limit Exceeded."""

    pass


class InternalServerError(APIStatusError):
    """HTTP 500+ Internal Server Error."""

    pass


class OfflineDataNotAvailableError(DojoError):
    """Offline data is not available for the requested endpoint or parameters."""

    pass
