from apis.mal import get_anime_url
from apis.anilist import search_anime

async def search(query: str):
    res = await search_anime(query)

    mal_url = get_anime_url(res['data']['Page']['media'][0]['idMal'])

    res['data']['Page']['media'][0]['extra_urls'] = {"mal": mal_url}

    return res