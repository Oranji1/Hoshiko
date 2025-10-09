from urllib.parse import parse_qs

from apis.anilist import search_anime
from apis.mal import get_anime
from core.models.anime import Anime, AnimeAiringInfo, SitesURLs
from core.models.enums import AiringStatus, MediaType, SourceType


async def search(query: str) -> Anime:
    res = await search_anime(query)
    res_anime = res["data"]["Page"]["media"][0]

    mal = await get_anime(res_anime["idMal"])
    mal = mal["data"]

    model = Anime(
        title=mal["title"],
        synopsis=mal["synopsis"],
        cover_url=mal["images"]["webp"]["large_image_url"],
        type=MediaType(mal["type"]),
        source=SourceType(mal["source"]),
        episodes=res_anime["episodes"],
        airing_info=AnimeAiringInfo(status=AiringStatus(mal["status"])),
    )

    urls = SitesURLs(mal=mal["url"], anilist=res_anime["siteUrl"])

    for ext_url in mal["external"]:
        url_name = ext_url["name"].lower()

        if url_name == "anidb":
            anidb_url = ext_url["url"]
            query_params = parse_qs(anidb_url)

            if "aid" in query_params:
                anidb_id = query_params["aid"][0]
                urls.anidb = f"https://anidb.net/anime/{anidb_id}"
            else:
                urls.anidb = ext_url["url"]
        elif url_name == "ann":
            urls.ann = ext_url["url"]

    model.sites_urls = urls

    return model
