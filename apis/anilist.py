from __future__ import annotations

from typing import TYPE_CHECKING

from core.constants import APIS

from ._session import AsyncSession

if TYPE_CHECKING:
    from niquests import Response


async def make_anilist_request(json: dict, headers: dict) -> Response:
    async with AsyncSession(APIS.anilist.name) as session:
        return await session.post(APIS.anilist.base_url, json=json, headers=headers)


async def search_anime(query: str) -> dict:
    graphql_query = """query ($search: String) {
        Media(search: $search, type: ANIME) {
            idMal
            episodes
            siteUrl
        }
    }"""

    res = await make_anilist_request(
        json={"query": graphql_query, "variables": {"search": query}},
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    return res.json()


async def search_manga(query: str) -> dict:
    graphql_query = """query ($search: String) {
        Media(search: $search, type: MANGA) {
            idMal
            chapters
            volumes
            siteUrl
        }
    }"""

    res = await make_anilist_request(
        json={"query": graphql_query, "variables": {"search": query}},
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    return res.json()
