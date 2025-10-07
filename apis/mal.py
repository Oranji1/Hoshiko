from jikanpy import AioJikan


async def search_anime(query: str):
    async with AioJikan() as jikan:
        result = await jikan.search(search_type="anime", query=query, page=1)
        return result


async def get_anime(id: int):
    async with AioJikan() as jikan:
        anime = await jikan.anime(id, extension="full")
        return anime

def get_anime_url(id: int):
    return f"https://myanimelist.net/anime/{id}"