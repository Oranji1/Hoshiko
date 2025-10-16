from datetime import date, time
from typing import Annotated, Literal

from pydantic import AfterValidator, HttpUrl
from pydantic.types import PositiveInt

from core.models.base_model import BaseModel
from core.models.enums import AiringStatus, MediaType, SourceType


def check_host(url: HttpUrl, allowed_host: str) -> HttpUrl:
    if url.host != allowed_host:
        msg = f"Invalid host URL. Expected '{allowed_host}', got '{url.host}'."
        raise TypeError(msg)
    return url


def host_url_validator(host: str) -> AfterValidator:
    return AfterValidator(lambda url: check_host(url, host))


class SitesURLs(BaseModel):
    anidb: Annotated[HttpUrl, host_url_validator("anidb.net")] | None = None
    anilist: Annotated[HttpUrl, host_url_validator("anilist.co")] | None = None
    ann: Annotated[HttpUrl, host_url_validator("www.animenewsnetwork.com")] | None = None
    mal: Annotated[HttpUrl, host_url_validator("myanimelist.net")] | None = None


class AnimeAiringInfo(BaseModel):
    status: AiringStatus | None = AiringStatus.NOT_YET_AIRED
    start: date | None = None
    end: date | None = None
    broadcast: time | None = None
    season: Literal["spring", "summer", "fall", "winter"] | None = None


class Anime(BaseModel):
    title: str
    synopsis: str | None = None
    cover_url: Annotated[HttpUrl, host_url_validator("cdn.myanimelist.net")] | None
    type: MediaType
    source: SourceType
    episodes: PositiveInt | None = None
    alt_titles: dict[str, str] = {}  # noqa: RUF012
    synonyms: list[str] = []  # noqa: RUF012
    airing_info: AnimeAiringInfo
    sites_urls: SitesURLs | None = None
