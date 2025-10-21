from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from cachetools import LRUCache
from rapidfuzz import fuzz, process

if TYPE_CHECKING:
    from core.models.anime import Anime


def make_uuid() -> str:
    return str(uuid.uuid4())


class CacheManager:  # Yes, this is horrible, I know
    def __init__(self, maxsize: int = 512) -> None:
        class SyncedLRUCache(LRUCache):
            def __init__(
                self, parent: CacheManager, *args: tuple, **kwargs: dict[str, str]
            ) -> None:
                super().__init__(*args, **kwargs)
                self._parent = parent

            def popitem(self) -> tuple[Any, Any]:
                key, value = super().popitem()
                self._parent._remove_titles_for(key)  # noqa: SLF001
                return key, value

        self.main_cache = SyncedLRUCache(self, maxsize=maxsize)
        self.title_cache: dict[str, str] = {}

    def _remove_titles_for(self, identifier: str) -> None:
        to_remove = [k for k, v in self.title_cache.items() if v == identifier]
        for k in to_remove:
            del self.title_cache[k]

    def add(self, model: Anime) -> str:
        cache_id = make_uuid()
        self.main_cache[cache_id] = model.model_dump()

        for title in model.alt_titles.values():
            if title not in self.title_cache:
                self.title_cache[title.lower()] = cache_id

        for synonym in model.synonyms:
            if synonym not in self.title_cache:
                self.title_cache[synonym.lower()] = cache_id

        return cache_id

    def get_by_id(self, cache_id: str) -> Anime | None:
        return self.main_cache.get(cache_id)

    def get_by_title(self, title: str) -> Anime | None:
        title = title.lower()

        if cache_id := self.title_cache.get(title):
            return self.main_cache.get(cache_id)

        result = process.extractOne(
            title,
            self.title_cache.keys(),
            scorer=fuzz.WRatio,
            score_cutoff=80,
        )

        if result:
            result = self.title_cache.get(result[0])
        return self.main_cache.get(result)
