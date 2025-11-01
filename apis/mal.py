import niquests


async def get_anime(id: int) -> dict:
    async with niquests.AsyncSession() as session:
        url = f"https://api.jikan.moe/v4/anime/{id}/full"
        response = await session.get(url=url)

        return response.json()


async def get_manga(id: int) -> dict:
    async with niquests.AsyncSession() as session:
        url = f"https://api.jikan.moe/v4/manga/{id}/full"
        response = await session.get(url=url)

        return response.json()
