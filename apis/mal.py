from jikanpy import AioJikan


async def get_anime(mal_id: int) -> dict:
    async with AioJikan() as jikan:
        return await jikan.anime(mal_id, extension="full")


async def get_manga(mal_id: int) -> dict:
    async with AioJikan() as jikan:
        return await jikan.manga(mal_id, extension="full")
