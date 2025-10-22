from .anilist import search_anime as search_anilist_anime
from .anilist import search_manga as search_anilist_manga
from .mal import get_anime as get_mal_anime
from .mal import get_manga as get_mal_manga

__all__ = ["get_mal_anime", "get_mal_manga", "search_anilist_anime", "search_anilist_manga"]
