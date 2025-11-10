from msgspec import convert

from apis import get_mal_anime, search_anilist_anime
from core.constants import DATABASES
from core.errors import NotFoundError
from core.structs import AiringStatus, Anime, AnimeAiringInfo, AnimeSitesURLs, MediaType, SourceType
from core.utils import clean_anidb_url

from .abc import BaseService


class AnimeService(BaseService):
    async def search(self, query: str, *, check_cached: bool = True) -> Anime:
        cached_anime = self.cache.get_by_title("anime", query) if check_cached else None
        if cached_anime:
            return convert(cached_anime, Anime)

        anilist_response = await search_anilist_anime(query)
        media = anilist_response.get("data", {}).get("Page", {}).get("media", [])

        if not media:
            raise NotFoundError(DATABASES.anilist, query)

        anilist_data = media[0]
        mal_id = anilist_data.get("idMal")

        if not mal_id:
            raise NotFoundError(DATABASES.anilist, query)

        mal_response = await get_mal_anime(mal_id)
        mal_data = mal_response.get("data")

        airing_info = AnimeAiringInfo(
            status=AiringStatus(mal_data["status"]), season=mal_data["season"]
        )

        urls_dict = {}
        urls_dict["anilist"] = anilist_data.get("siteUrl")
        urls_dict["mal"] = mal_data["url"]

        for link_data in mal_data["external"]:
            site_name = link_data["name"].lower()
            url = link_data["url"]

            if not url:
                continue

            if site_name == "anidb":
                urls_dict["anidb"] = clean_anidb_url(url)
            elif site_name == "ann":
                urls_dict["ann"] = url

        sites_urls = convert(urls_dict, AnimeSitesURLs)

        anime = Anime(
            title=mal_data.get("title", "N/A"),
            synopsis=mal_data.get("synopsis", "N/A"),
            cover_url=mal_data["images"]["webp"].get("large_image_url"),
            type=MediaType(mal_data["type"]),
            source=SourceType(mal_data.get("source", "OTHER")),
            episodes=anilist_data.get("episodes"),
            titles=mal_data["titles"],
            airing_info=airing_info,
            sites_urls=sites_urls,
        )

        self.cache.add("anime", anime)

        return anime
