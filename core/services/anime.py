from apis import get_mal_anime, search_anilist_anime
from core import CacheManager
from core.errors import APIError, ResourceNotFoundError, SearchNotFoundError
from core.models import AiringStatus, Anime, AnimeAiringInfo, MediaType, SitesURLs, SourceType
from core.utils import clean_anidb_url


async def search(query: str, cache: CacheManager) -> Anime:
    if cached_anime := cache.get_by_title(query):
        return Anime.model_validate(cached_anime)

    # I know this all looks awful, I'll rewrite it in v0.2
    try:
        anilist_response = await search_anilist_anime(query)
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
        mal_response = await get_mal_anime(mal_id)
        mal_data = mal_response.get("data")
    except Exception as e:
        raise APIError("MyAnimeList", str(e)) from e  # noqa: EM101

    if not mal_data:
        raise SearchNotFoundError(query, "MyAnimeList")

    model = Anime(
        title=mal_data.get("title", "N/A"),
        synopsis=mal_data.get("synopsis"),
        cover_url=mal_data.get("images").get("webp").get("large_image_url"),
        type=MediaType(mal_data.get("type")),
        source=SourceType(mal_data.get("source", "OTHER")),
        episodes=anilist_data.get("episodes"),
        airing_info=AnimeAiringInfo(status=AiringStatus(mal_data.get("status"))),
    )

    for t in mal_data.get("titles"):
        title_type = t["type"]
        title = t["title"]

        if title_type.lower() == "synonym":
            model.synonyms.append(title)
            continue

        model.alt_titles[title_type] = title

    sites_urls = SitesURLs(anilist=anilist_data.get("siteUrl"), mal=mal_data.get("url"))
    external_links = mal_data.get("external", [])
    for link_data in external_links:
        site_name = link_data.get("name", "").lower()
        url = link_data.get("url")

        if not url:
            continue

        if site_name == "anidb":
            sites_urls.anidb = clean_anidb_url(url)
        elif site_name == "ann":
            sites_urls.ann = url

    model.sites_urls = sites_urls

    cache.add(model)

    return model
