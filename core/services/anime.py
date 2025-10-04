from apis.mal import search_anime

async def search(query: str):
    return await search_anime(query)