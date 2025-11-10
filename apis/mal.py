import logging

import niquests

from core.constants import APIS
from core.errors import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)

logger = logging.getLogger(__name__)


async def make_jikan_request(cat: str, id: int, ext: str | None = None) -> niquests.Response:
    url = f"{APIS.jikan.base_url}/{cat}/{id}" + (f"/{ext}" if ext else "")
    name = APIS.jikan.name

    async with niquests.AsyncSession() as session:
        res = await session.get(url)
        status = res.status_code

        if status == 400:
            raise BadRequestError(name)
        elif status == 404:  # noqa: RET506
            raise NotFoundError(name, resource=f"{cat}/{id}")
        elif status == 429:
            raise RateLimitError(name)
        elif status == 500:
            raise InternalServerError(name)
        elif status == 503:
            raise ServiceUnavailableError(name)

        return res


async def get_anime(id: int) -> dict:
    res = await make_jikan_request("anime", id, "full")
    return res.json()


async def get_manga(id: int) -> dict:
    res = await make_jikan_request("manga", id, "full")
    return res.json()
