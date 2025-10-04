from jikanpy import AioJikan

async def search_anime(query: str):
    async with AioJikan() as aio_jikan:
        result = await aio_jikan.search(search_type='anime', query=query, page=1)
        return result