from datetime import date
from typing import Annotated

from msgspec import Meta, structs

from core.errors import URLValidationError
from core.utils import http_url_validator

from .base_struct import BaseMediaStruct, BaseStruct
from .enums import PublicationStatus

ALLOWED_HOSTS = {
    "anilist": "anilist.co",
    "mal": "myanimelist.net",
}


class MangaSitesURLs(BaseStruct, kw_only=True):
    anilist: str | None = None
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


class MangaPublicationInfo(BaseStruct, kw_only=True):
    status: PublicationStatus | None = PublicationStatus.NOT_YET_PUBLISHED
    start: date | None = None
    end: date | None = None


class Manga(BaseMediaStruct, kw_only=True):
    chapters: Annotated[int, Meta(ge=0)] | None = None
    volumes: Annotated[int, Meta(ge=0)] | None = None
    publication_info: MangaPublicationInfo
    sites_urls: MangaSitesURLs | None = None
