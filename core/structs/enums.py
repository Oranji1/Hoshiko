from enum import StrEnum
from typing import Any


class BaseStrEnum(StrEnum):
    @classmethod
    def _missing_(cls, value: str) -> Any:  # noqa: ANN401
        value = value.lower()
        for member in cls:
            if member.value.lower() == value:
                return member
        return super()._missing_(value)


class AiringStatus(BaseStrEnum):
    AIRING = "Currently airing"
    FINISHED = "Finished airing"
    NOT_YET_AIRED = "Not yet aired"


class PublicationStatus(BaseStrEnum):
    PUBLISING = "Publishing"
    FINISHED = "Finished"
    HIATUS = "On hiatus"
    NOT_YET_PUBLISHED = "Not yet published"


class MediaType(BaseStrEnum):
    TV = "TV"
    MOVIE = "Movie"
    OVA = "OVA"
    ONA = "ONA"
    SPECIAL = "Special"
    MANGA = "Manga"
    ONE_SHOT = "One-shot"
    DOUJINSHI = "Doujinshi"
    LIGHT_NOVEL = "Light Novel"
    NOVEL = "Novel"
    MANHWA = "Manhwa"
    MANHUA = "Manhua"


class SourceType(BaseStrEnum):
    ORIGINAL = "Original"
    MANGA = "Manga"
    NOVEL = "Novel"
    LIGHT_NOVEL = "Light Novel"
    VISUAL_NOVEL = "Visual Novel"
    GAME = "Game"
    OTHER = "Other"
