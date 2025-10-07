from apis.mal import get_anime
from apis.anilist import search_anime
from urllib.parse import parse_qs

async def search(query: str):
    res = await search_anime(query)
    anime = res['data']['Page']['media'][0]

    mal = await get_anime(anime['idMal'])
    mal = mal['data']

    anime['synopsis'] = mal['synopsis']

    extra_urls = anime['extra_urls'] = {}
    extra_urls['mal'] = mal['url']

    for ext_url in mal['external']:
        url_name = ext_url['name'].lower()

        if url_name == "anidb":
            anidb_url = ext_url['url']
            query_params = parse_qs(anidb_url)

            if 'aid' in query_params:
                anidb_id = query_params['aid'][0]
                extra_urls['anidb'] = f"https://anidb.net/anime/{anidb_id}"
            else:
                extra_urls['anidb'] = ext_url['url']
        elif url_name == "ann":
            extra_urls['ann'] = ext_url['url']
    
    return anime