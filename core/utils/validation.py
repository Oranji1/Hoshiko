from pydantic import AfterValidator, HttpUrl

from core.errors import HostValidationError


def check_host(url: HttpUrl, allowed_host: str) -> HttpUrl:
    if url.host != allowed_host:
        raise HostValidationError(allowed_host, url.host)
    return url


def host_url_validator(host: str) -> AfterValidator:
    return AfterValidator(lambda url: check_host(url, host))
