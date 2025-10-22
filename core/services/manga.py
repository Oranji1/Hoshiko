from apis import get_mal_manga, search_anilist_manga
from core import CacheManager
from core.errors import APIError, ResourceNotFoundError, SearchNotFoundError
from core.models import Manga, MangaPublicationInfo, MangaSitesURLs, MediaType, PublicationStatus


async def search(query: str, cache: CacheManager) -> Manga:
    if cached_anime := cache.get_by_title("manga", query):
        return Manga.model_validate(cached_anime)

    # I know this all looks awful, I'll rewrite it in v0.2
    try:
        anilist_response = await search_anilist_manga(query)
        media = anilist_response.get("data", {}).get("Page", {}).get("media", [])
    except Exception as e:
        raise APIError("AniList", str(e)) from e  # noqa: EM101 # I'll properly handle these linter's errors later

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

    if not mal_data:
        raise SearchNotFoundError(query, "MyAnimeList")

    sites_urls = MangaSitesURLs(anilist=anilist_data.get("siteUrl"), mal=mal_data.get("url"))

    model = Manga(
        title=mal_data.get("title", "N/A"),
        synopsis=mal_data.get("synopsis"),
        cover_url=mal_data.get("images").get("webp").get("large_image_url"),
        type=MediaType(mal_data.get("type")),
        chapters=anilist_data.get("chapters"),
        volumes=anilist_data.get("volumes"),
        publication_info=MangaPublicationInfo(status=PublicationStatus(mal_data.get("status"))),
        sites_urls=sites_urls,
    )

    for t in mal_data.get("titles"):
        title_type = t["type"]
        title = t["title"]

        if title_type.lower() == "synonym":
            model.synonyms.append(title)
            continue

        model.alt_titles[title_type] = title

    cache.add("manga", model)

    return model
