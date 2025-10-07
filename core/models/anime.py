from pydantic import BaseModel as PydanticBaseModel
from pydantic import ConfigDict
from typing import Literal, Optional
from base_models import MediaType

class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_default=True)

class SitesURLs(BaseModel):
    anidb: Optional[str]
    anilist: Optional[str]
    ann: Optional[str]
    mal: Optional[str]

class AnimeAiringInfo(BaseModel):
    status: Literal["airing", "finished_airing"] #### ?
    start: str ####
    end: str ####
    season: Literal["spring", "summer", "fall", "winter"]

class Anime(BaseModel):
    title: str
    synopsis: str
    type: MediaType
    source: MediaType
    episodes: Optional[int] = None
    alt_titles: str  ####
    synonims: str  ####
    airing_info: AnimeAiringInfo
    sites_urls: SitesURLs
