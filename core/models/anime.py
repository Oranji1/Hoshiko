from datetime import date, time
from typing import Annotated, Literal, Optional

from pydantic import AfterValidator, BaseModel, HttpUrl
from pydantic.types import PositiveInt

from core.models.base_model import BaseModel
from core.models.enums import AiringStatus, MediaType, SourceType


def check_host(url: HttpUrl, allowed_host: str) -> HttpUrl:
    if url.host != allowed_host:
        raise TypeError(
            f"Invalid host URL. Expected '{allowed_host}', got '{url.host}'."
        )
    return url


def host_url_validator(host: str):
    return AfterValidator(lambda url: check_host(url, host))


class SitesURLs(BaseModel):
    anidb: Optional[Annotated[HttpUrl, host_url_validator("anidb.net")]] = None
    anilist: Optional[Annotated[HttpUrl, host_url_validator("anilist.co")]] = None
    ann: Optional[
        Annotated[HttpUrl, host_url_validator("www.animenewsnetwork.com")]
    ] = None
    mal: Optional[Annotated[HttpUrl, host_url_validator("myanimelist.net")]] = None


class AnimeAiringInfo(BaseModel):
    status: Optional[AiringStatus] = AiringStatus.NOT_YET_AIRED
    start: Optional[date] = None
    end: Optional[date] = None
    broadcast: Optional[time] = None
    season: Optional[Literal["spring", "summer", "fall", "winter"]] = None


class Anime(BaseModel):
    title: str
    synopsis: Optional[str] = None
    type: MediaType
    source: SourceType
    episodes: Optional[PositiveInt] = None
    alt_titles: list[str] = []
    synonyms: list[str] = []
    airing_info: AnimeAiringInfo
    sites_urls: Optional[SitesURLs] = None
