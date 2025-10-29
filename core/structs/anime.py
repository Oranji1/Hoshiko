from datetime import date, time
from typing import Annotated, Literal

from msgspec import Meta, field, structs

from core.errors import URLValidationError
from core.utils import http_url_validator

from .base_struct import BaseStruct
from .enums import AiringStatus, MediaType, SourceType

ALLOWED_HOSTS = {
    "anidb": "anidb.net",
    "anilist": "anilist.co",
    "ann": "www.animenewsnetwork.com",
    "mal": "myanimelist.net",
}


class AnimeSitesURLs(BaseStruct, kw_only=True):
    anidb: str | None = None
    anilist: str | None = None
    ann: str | None = None
    mal: str | None = None

    def __post_init__(self) -> None:
        for field in self.__struct_fields__:  # noqa: F402
            url = getattr(self, field)
            if url is None:
                continue
            try:
                http_url_validator(url, allowed_host=ALLOWED_HOSTS[field])
            except URLValidationError:
                structs.force_setattr(self, field, None)


class AnimeAiringInfo(BaseStruct, kw_only=True):
    status: AiringStatus | None = AiringStatus.NOT_YET_AIRED
    start: date | None = None
    end: date | None = None
    broadcast: time | None = None
    season: Literal["spring", "summer", "fall", "winter"] | None = "N/A"


class Anime(BaseStruct, kw_only=True):
    title: str
    synopsis: str | None = "N/A"
    cover_url: str | None = None
    type: MediaType
    source: SourceType
    episodes: Annotated[int, Meta(ge=0)] | None = None
    titles: list[dict[str, str]] | None = field(default_factory=list)
    airing_info: AnimeAiringInfo
    sites_urls: AnimeSitesURLs | None = None

    def __post_init__(self) -> None:
        cover_url = self.cover_url

        if not cover_url:
            pass
        try:
            http_url_validator(cover_url, allowed_host="cdn.myanimelist.net")
        except URLValidationError:
            structs.force_setattr(self, "cover_url", None)
