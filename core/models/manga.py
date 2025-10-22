from datetime import date
from typing import Annotated

from pydantic import HttpUrl
from pydantic.types import PositiveInt

from core.utils import host_url_validator

from .base_model import BaseModel
from .enums import MediaType, PublicationStatus


class MangaSitesURLs(BaseModel):
    anilist: Annotated[HttpUrl, host_url_validator("anilist.co")] | None = None
    mal: Annotated[HttpUrl, host_url_validator("myanimelist.net")] | None = None


class MangaPublicationInfo(BaseModel):
    status: PublicationStatus | None = PublicationStatus.NOT_YET_PUBLISHED
    start: date | None = None
    end: date | None = None


class Manga(BaseModel):
    title: str
    synopsis: str | None = None
    cover_url: Annotated[HttpUrl, host_url_validator("cdn.myanimelist.net")] | None
    type: MediaType
    chapters: PositiveInt | None = None
    volumes: PositiveInt | None = None
    alt_titles: dict[str, str] = {}  # noqa: RUF012
    synonyms: list[str] = []  # noqa: RUF012
    publication_info: MangaPublicationInfo
    sites_urls: MangaSitesURLs | None = None
