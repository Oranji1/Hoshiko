import logging

import niquests

from core.errors import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)

logger = logging.getLogger(__name__)

BASE_URL = "https://api.jikan.moe/v4/"


async def make_jikan_request(cat: str, id: int, ext: str | None = None) -> niquests.Response:
    url = f"{BASE_URL}/{cat}/{id}" + (f"/{ext}" if ext else "")

    async with niquests.AsyncSession() as session:
        res = await session.get(url)
        status = res.status_code

        if status == 400:
            raise BadRequestError("Jikan")  # noqa: EM101
        elif status == 404:  # noqa: RET506
            raise NotFoundError("Jikan", resource=f"{cat}/{id}")  # noqa: EM101
        elif status == 429:
            raise RateLimitError("Jikan")  # noqa: EM101
        elif status == 500:
            raise InternalServerError("Jikan")  # noqa: EM101
        elif status == 503:
            raise ServiceUnavailableError("Jikan")  # noqa: EM101

        return res


async def get_anime(id: int) -> dict:
    res = await make_jikan_request("anime", id, "full")
    return res.json()


async def get_manga(id: int) -> dict:
    res = await make_jikan_request("manga", id, "full")
    return res.json()
