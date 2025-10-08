from datetime import date, time
from typing import Literal, Optional

from pydantic.types import PositiveInt

from core.models.base_model import BaseModel
from core.models.enums import AiringStatus, MediaType, SourceType


class SitesURLs(BaseModel):
    anidb: Optional[str] = None
    anilist: Optional[str] = None
    ann: Optional[str] = None
    mal: Optional[str] = None


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
