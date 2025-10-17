class HoshikoError(Exception):
    pass


class APIError(HoshikoError):
    def __init__(self, source: str, detail: str | None = None) -> None:
        msg = f"Error communicating with {source} API"
        if detail:
            msg += f" ({detail})"
        super().__init__(msg)


class NotFoundError(HoshikoError):
    def __init__(self, query: str, source: str | None = None, context: str | None = None) -> None:
        msg = f"No results found for '{query}'"
        if source:
            msg += f" in {source}"
        if context:
            msg += f" ({context})"
        super().__init__(msg)


class SearchNotFoundError(NotFoundError):
    def __init__(self, query: str, source: str) -> None:
        super().__init__(query, source, context="search")


class ResourceNotFoundError(NotFoundError):
    def __init__(self, resource: str, source: str, query: str) -> None:
        msg = f"Missing {resource} for '{query}' from {source}"
        super().__init__(query, source, context=msg)


class ValidationError(HoshikoError):
    pass


class HostValidationError(HoshikoError):
    def __init__(self, expected_host: str, actual_host: str) -> None:
        msg = f"Invalid host URL: expected '{expected_host}', got '{actual_host}'"
        super().__init__(msg)
