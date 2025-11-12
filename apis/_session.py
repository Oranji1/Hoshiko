from __future__ import annotations

import time
from typing import TYPE_CHECKING

from niquests import AsyncSession as NiqAsyncSession

from core.errors import (
    APIClientError,
    APIServerError,
    BadRequestError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
    ServiceUnavailableError,
)

if TYPE_CHECKING:
    from niquests import Response


class AsyncSession(NiqAsyncSession):
    def __init__(
        self, source_name: str, max_calls: int, period: float = 60.0, *args, **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.source_name = source_name

        # Rate limiter state
        self._max_calls = max_calls
        self._remaining = max_calls
        self._window = 0.0
        self._period = period

    def _ensure_not_rate_limited(self) -> None:
        current = time.time()

        if current > self._window + self._period:
            self._remaining = self._max_calls

        if self._remaining == self._max_calls:
            self._window = current

        if self._remaining == 0:
            retry_after = f"{(self._period - (current - self._window)):.2f}s"
            raise RateLimitError(self.source_name, retry_after)

        self._remaining -= 1

    def _check_errors(self, res: Response) -> None:
        status = res.status_code

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
        elif status >= 400 and status <= 499:
            raise APIClientError(self.source_name, status, "Unhandled error")
        elif status >= 500:
            raise APIServerError(self.source_name, status, "Unhladed error")

    async def request(self, *args, **kwargs) -> Response:
        self._ensure_not_rate_limited()

        res = await super().request(*args, **kwargs)

        self._check_errors(res)

        return res
