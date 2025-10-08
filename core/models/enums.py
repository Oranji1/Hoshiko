from enum import Enum


class AiringStatus(str, Enum):
    AIRING = "Currently airing"
    FINISHED = "Finished airing"
    NOT_YET_AIRED = "Not yet aired"


class MediaType(str, Enum):
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


class SourceType(str, Enum):
    ORIGINAL = "Original"
    MANGA = "Manga"
    LIGHT_NOVEL = "Light Novel"
    VISUAL_NOVEL = "Visual Novel"
    GAME = "Game"
    OTHER = "Other"
