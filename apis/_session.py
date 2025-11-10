from __future__ import annotations

from typing import TYPE_CHECKING

from niquests import AsyncSession as NiqAsyncSession

from core.errors import (
    BadRequestError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)

if TYPE_CHECKING:
    from niquests import Response


class AsyncSession(NiqAsyncSession):
    def __init__(self, source_name: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.source_name = source_name

    async def request(self, *args, **kwargs) -> Response:
        res = await super().request(*args, **kwargs)
        status = res.status_code

        # TODO: I should do some parsing to add more context to the errors
        if status == 400:
            raise BadRequestError(self.source_name)
        elif status == 404:  # noqa: RET506
            raise NotFoundError(self.source_name)
        elif status == 429:
            raise RateLimitError(self.source_name)
        elif status == 500:
            raise InternalServerError(self.source_name)
        elif status == 503:
            raise ServiceUnavailableError(self.source_name)

        return res
