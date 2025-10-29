from datetime import date
from typing import Annotated

from msgspec import Meta, field, structs

from core.errors import URLValidationError
from core.utils import http_url_validator

from .base_struct import BaseStruct
from .enums import MediaType, PublicationStatus

ALLOWED_HOSTS = {
    "anilist": "anilist.co",
    "mal": "myanimelist.net",
}


class MangaSitesURLs(BaseStruct, kw_only=True):
    anilist: str | None = None
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


class MangaPublicationInfo(BaseStruct, kw_only=True):
    status: PublicationStatus | None = PublicationStatus.NOT_YET_PUBLISHED
    start: date | None = None
    end: date | None = None


class Manga(BaseStruct, kw_only=True):
    title: str
    synopsis: str | None = "N/A"
    cover_url: str | None = None
    type: MediaType
    chapters: Annotated[int, Meta(ge=0)] | None = None
    volumes: Annotated[int, Meta(ge=0)] | None = None
    titles: list[dict[str, str]] | None = field(default_factory=list)
    publication_info: MangaPublicationInfo
    sites_urls: MangaSitesURLs | None = None

    def __post_init__(self) -> None:
        cover_url = self.cover_url

        if not cover_url:
            pass
        try:
            http_url_validator(cover_url, allowed_host="cdn.myanimelist.net")
        except URLValidationError:
            structs.force_setattr(self, "cover_url", None)
