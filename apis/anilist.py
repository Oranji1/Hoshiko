import niquests


async def search_anime(query: str) -> dict:
    graphql_query = """query ($search: String!) {
        Page(page: 1, perPage: 1) {
            media(search: $search, type: ANIME) {
                idMal
                episodes
                siteUrl
            }
        }
    }"""
    async with niquests.AsyncSession() as session:
        variables = {"search": query}
        response = await session.post(
            url="https://graphql.anilist.co",
            json={"query": graphql_query, "variables": variables},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        return response.json()


async def search_manga(query: str) -> dict:
    graphql_query = """query ($search: String!) {
        Page(page: 1, perPage: 1) {
            media(search: $search, type: MANGA) {
                idMal
                chapters
                volumes
                siteUrl
            }
        }
    }"""
    async with niquests.AsyncSession() as session:
        variables = {"search": query}
        response = await session.post(
            url="https://graphql.anilist.co",
            json={"query": graphql_query, "variables": variables},
            headers={"Content-Type": "application/json", "Accept": "application/json"},
        )

        return response.json()
