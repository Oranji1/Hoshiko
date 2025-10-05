import niquests


async def search_anime(query: str) -> dict:
    graphql_query = """query ($search: String!) {
        Page(page: 1, perPage: 1) {
            media(search: $search, type: ANIME) {
                id
                idMal
                title {
                    romaji
                    english
                    native
                }
                coverImage {
                    large
                }
                description
                format
                episodes
                source
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
