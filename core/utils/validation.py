from urllib.parse import urlparse

from core.errors import HostValidationError, HTTPUrlValidationError


def http_url_validator(url: str, *, allowed_host: str | None = None) -> None:
    parsed = urlparse(url)

    if parsed.scheme in {"http", "https"} and bool(parsed.netloc):
        if allowed_host is not None and parsed.hostname != allowed_host:
            raise HostValidationError(allowed_host, parsed.hostname)
        return
    raise HTTPUrlValidationError(url)
