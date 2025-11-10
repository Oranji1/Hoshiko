from typing import NamedTuple


class DatabaseInfo(NamedTuple):
    name: str
    abbreviation: str
    hostname: str


class APIInfo(NamedTuple):
    name: str
    base_url: str


class DATABASES:
    anilist = DatabaseInfo("AniList", "ANL", "anilist.co")
    anidb = DatabaseInfo("AniDB", "ADB", "anidb.co")
    ann = DatabaseInfo("Anime News Network", "ANN", "animenewsnetwork.com")
    kitsu = DatabaseInfo("Kitsu", "KIT", "kitsu.app")
    mal = DatabaseInfo("MyAnimeList", "MAL", "myanimelist.net")


class APIS:
    anilist = APIInfo("AniList", "https://graphql.anilist.co")
    jikan = APIInfo("Jikan", "https://api.jikan.moe/v4")
    kitsu = APIInfo("Kitsu", "https://kitsu.io/api/edge")
