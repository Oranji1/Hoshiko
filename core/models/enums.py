from enum import Enum


class BaseStrEnum(str, Enum):
    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            value = value.lower()
            for member in cls:
                if member.value.lower() == value:
                    return member
        return super()._missing_(value)


class AiringStatus(BaseStrEnum):
    AIRING = "Currently airing"
    FINISHED = "Finished airing"
    NOT_YET_AIRED = "Not yet aired"


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
    LIGHT_NOVEL = "Light Novel"
    VISUAL_NOVEL = "Visual Novel"
    GAME = "Game"
    OTHER = "Other"
