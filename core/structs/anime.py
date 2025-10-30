from datetime import date, time
from typing import Annotated, Literal

from msgspec import Meta, structs

from core.errors import URLValidationError
from core.utils import http_url_validator

from .base_struct import BaseMediaStruct, BaseStruct
from .enums import AiringStatus, SourceType

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
        for field in self.__struct_fields__:
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


class Anime(BaseMediaStruct, kw_only=True):
    source: SourceType
    episodes: Annotated[int, Meta(ge=0)] | None = None
    airing_info: AnimeAiringInfo
    sites_urls: AnimeSitesURLs | None = None
