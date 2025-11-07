from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core import CacheManager
    from core.structs import BaseStruct


class BaseService(abc.ABC):
    def __init__(self, cache_manager: CacheManager) -> None:
        self._cache = cache_manager

    @property
    def cache(self) -> CacheManager:
        return self._cache

    @abc.abstractmethod
    async def search(self, query: str, *, check_cached: bool = True) -> BaseStruct:
        raise NotImplementedError
