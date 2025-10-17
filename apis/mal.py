from jikanpy import AioJikan

# async def search_anime(query: str) -> dict:
#     async with AioJikan() as jikan:
#         return await jikan.search(search_type="anime", query=query, page=1)


async def get_anime(mal_id: int) -> dict:
    async with AioJikan() as jikan:
        return await jikan.anime(mal_id, extension="full")
