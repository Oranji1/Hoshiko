from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from core.constants import APIS

from ._session import AsyncSession

if TYPE_CHECKING:
    from niquests import Response

logger = logging.getLogger(__name__)

jikan_session = AsyncSession(APIS.jikan.name, max_calls=90, period=90.0)


async def make_jikan_request(cat: str, id: int, ext: str | None = None) -> Response:
    url = f"{APIS.jikan.base_url}/{cat}/{id}" + (f"/{ext}" if ext else "")

    return await jikan_session.get(url)


async def get_anime(id: int) -> dict:
    res = await make_jikan_request("anime", id, "full")
    return res.json()


async def get_manga(id: int) -> dict:
    res = await make_jikan_request("manga", id, "full")
    return res.json()
