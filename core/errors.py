class HoshikoError(Exception):
    pass


class ValidationError(HoshikoError):
    pass


class URLValidationError(ValidationError):
    pass


class HTTPUrlValidationError(URLValidationError):
    def __init__(self, obtained_url: str) -> None:
        msg = f"Invalid URL: expected HTTP or HTTPS, got '{obtained_url}'"
        super().__init__(msg)


class HostValidationError(URLValidationError):
    def __init__(self, expected_host: str, actual_host: str) -> None:
        msg = f"Invalid host URL: expected '{expected_host}', got '{actual_host}'"
        super().__init__(msg)


class APIError(HoshikoError):
    def __init__(self, source: str, status_code: int, message: str) -> None:
        self.source = source
        self.status_code = status_code
        self.message = message

        super().__init__(f"[{source} API Error | HTTP {status_code}]: {message}")


class APIClientError(APIError):
    def __init__(self, source: str, status_code: int, message: str) -> None:
        super().__init__(source, status_code, message)


class APIServerError(APIError):
    def __init__(self, source: str, status_code: int, message: str) -> None:
        super().__init__(source, status_code, message)


class BadRequestError(APIClientError):
    def __init__(self, source: str, message: str = "Bad Request") -> None:
        super().__init__(source, 400, message)


class NotFoundError(APIClientError):
    def __init__(self, source: str, resource: str | None = None) -> None:
        msg = "Resource not found"
        if resource:
            msg += f" (Resource: {resource})"
        super().__init__(source, 404, msg)


class RateLimitError(APIClientError):
    def __init__(self, source: str, retry_after: str | int | None = None) -> None:
        msg = "Rate limit exceeded"
        if retry_after:
            msg += f": Retry after {retry_after}"

        self.retry_after = retry_after
        super().__init__(source, 429, msg)


class InternalServerError(APIServerError):
    def __init__(self, source: str, message: str = "Internal Server Error") -> None:
        super().__init__(source, 500, message)


class ServiceUnavailableError(APIServerError):
    def __init__(self, source: str, retry_after: str | int | None = None) -> None:
        msg = "Service Unavailable"
        if retry_after:
            msg += f": Retry after {retry_after}"

        self.retry_after = retry_after
        super().__init__(source, 503, msg)
