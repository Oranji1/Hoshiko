from msgspec import convert

from apis import get_mal_manga, search_anilist_manga
from core.constants import DATABASES
from core.errors import NotFoundError
from core.structs import Manga, MangaPublicationInfo, MangaSitesURLs, MediaType, PublicationStatus

from .abc import BaseService


class MangaService(BaseService):
    async def search(self, query: str, *, check_cached: bool = True) -> Manga:
        cached_manga = self.cache.get_by_title("manga", query) if check_cached else None
        if cached_manga:
            return convert(cached_manga, Manga)

        anilist_response = await search_anilist_manga(query)
        anilist_data = anilist_response["data"]["Media"]

        mal_id = anilist_data["idMal"]

        if not mal_id:
            raise NotFoundError(DATABASES.anilist.name, query)

        mal_response = await get_mal_manga(mal_id)
        mal_data = mal_response["data"]

        sites_urls = MangaSitesURLs(anilist=anilist_data["siteUrl"], mal=mal_data["url"])

        manga = Manga(
            title=mal_data["title"],
            synopsis=mal_data["synopsis"],
            cover_url=mal_data["images"]["webp"]["large_image_url"],
            type=MediaType(mal_data["type"]),
            chapters=mal_data["chapters"],
            volumes=mal_data["volumes"],
            titles=mal_data["titles"],
            publication_info=MangaPublicationInfo(status=PublicationStatus(mal_data["status"])),
            sites_urls=sites_urls,
        )

        self.cache.add("manga", manga)

        return manga
