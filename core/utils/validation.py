from pydantic import AfterValidator, HttpUrl


def check_host(url: HttpUrl, allowed_host: str) -> HttpUrl:
    if url.host != allowed_host:
        msg = f"Invalid host URL. Expected '{allowed_host}', got '{url.host}'."
        raise TypeError(msg)
    return url


def host_url_validator(host: str) -> AfterValidator:
    return AfterValidator(lambda url: check_host(url, host))
