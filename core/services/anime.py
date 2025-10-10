from urllib.parse import parse_qs, urlparse

from apis.anilist import search_anime
from apis.mal import get_anime
from core.models.anime import Anime, AnimeAiringInfo, SitesURLs
from core.models.enums import AiringStatus, MediaType, SourceType


def _clean_anidb_url(original_url: str) -> str:
    try:
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)

        if "aid" in query_params:
            anidb_id = query_params["aid"][0]
            return f"https://anidb.net/anime/{anidb_id}"
    except (ValueError, IndexError):
        pass

    return original_url


async def search(query: str) -> Anime:
    anilist_response = await search_anime(query)
    anilist_data = anilist_response.get("data").get("Page").get("media")[0]
    if not anilist_data:
        return None

    mal_id = anilist_data.get("idMal")

    if not mal_id:
        return None

    mal_response = await get_anime(mal_id)
    mal_data = mal_response.get("data")

    if not mal_data:
        return None

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
            sites_urls.anidb = _clean_anidb_url(url)
        elif site_name == "ann":
            sites_urls.ann = url

    model.sites_urls = sites_urls

    return model
