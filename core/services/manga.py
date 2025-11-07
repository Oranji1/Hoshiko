from msgspec import convert

from apis import get_mal_manga, search_anilist_manga
from core.errors import APIError, ResourceNotFoundError, SearchNotFoundError
from core.structs import Manga, MangaPublicationInfo, MangaSitesURLs, MediaType, PublicationStatus

from .abc import BaseService


class MangaService(BaseService):
    async def search(self, query: str, *, check_cached: bool = True) -> Manga:
        cached_manga = self.cache.get_by_title("manga", query) if check_cached else None
        if cached_manga:
            return convert(cached_manga, Manga)

        try:
            anilist_response = await search_anilist_manga(query)
            media = anilist_response.get("data", {}).get("Page", {}).get("media", [])
        except Exception as e:
            raise APIError("AniList", str(e)) from e  # noqa: EM101

        if not media:
            raise SearchNotFoundError(query, "AniList")

        anilist_data = media[0]
        mal_id = anilist_data.get("idMal")

        if not mal_id:
            raise ResourceNotFoundError("idMal", "AniList", query)  # noqa: EM101

        try:
            mal_response = await get_mal_manga(mal_id)
            mal_data = mal_response.get("data")
        except Exception as e:
            raise APIError("MyAnimeList", str(e)) from e  # noqa: EM101

        sites_urls = MangaSitesURLs(anilist=anilist_data.get("siteUrl"), mal=mal_data["url"])

        manga = Manga(
            title=mal_data.get("title", "N/A"),
            synopsis=mal_data.get("synopsis", "N/A"),
            cover_url=mal_data["images"]["webp"].get("large_image_url"),
            type=MediaType(mal_data["type"]),
            chapters=anilist_data["chapters"],
            volumes=anilist_data["volumes"],
            titles=mal_data["titles"],
            publication_info=MangaPublicationInfo(status=PublicationStatus(mal_data["status"])),
            sites_urls=sites_urls,
        )

        self.cache.add("manga", manga)

        return manga
