from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from cachetools import LRUCache
from rapidfuzz import fuzz, process

if TYPE_CHECKING:
    from core.models import Anime, Manga


def make_uuid() -> str:
    return str(uuid.uuid4())


class SyncedLRUCache(LRUCache):
    def __init__(
        self, parent: CacheManager, cache_type: str, *args: tuple, **kwargs: dict[str, str]
    ) -> None:
        super().__init__(*args, **kwargs)
        self._parent = parent
        self._type = cache_type

    def popitem(self) -> tuple:
        key, value = super().popitem()
        self._parent._remove_titles_for(self._type, key)  # noqa: SLF001
        return key, value


class CacheManager:  # Yes, this is horrible, I know
    def __init__(self, maxsize: int = 512) -> None:
        self.main_caches: dict[str, SyncedLRUCache] = {}
        self.title_caches: dict[str, dict[str, str]] = {}
        self.maxsize = maxsize

    def _ensure_cache(self, cache_type: str) -> None:
        if cache_type not in self.main_caches:
            self.main_caches[cache_type] = SyncedLRUCache(self, cache_type, maxsize=self.maxsize)
            self.title_caches[cache_type] = {}

    def _remove_titles_for(self, cache_type: str, identifier: str) -> None:
        title_cache = self.title_caches.get(cache_type, {})
        to_remove = [k for k, v in title_cache.items() if v == identifier]
        for k in to_remove:
            del title_cache[k]

    def add(self, cache_type: str, model: Anime | Manga) -> str:
        self._ensure_cache(cache_type)

        cache_id = make_uuid()
        self.main_caches[cache_type][cache_id] = model.model_dump()

        title_cache = self.title_caches[cache_type]

        for title in model.alt_titles.values():
            if title not in title_cache:
                title_cache[title.lower()] = cache_id

        for synonym in model.synonyms:
            if synonym not in title_cache:
                title_cache[synonym.lower()] = cache_id

        return cache_id

    def get_by_id(self, cache_type: str, cache_id: str) -> dict | None:
        cache = self.main_caches.get(cache_type)
        return cache.get(cache_id) if cache else None

    def get_by_title(self, cache_type: str, title: str) -> dict | None:
        self._ensure_cache(cache_type)

        title_cache = self.title_caches.get(cache_type, {})
        main_cache = self.main_caches.get(cache_type, {})

        if cache_id := title_cache.get(title):
            return main_cache.get(cache_id)

        result = process.extractOne(
            title.lower(), title_cache.keys(), scorer=fuzz.WRatio, score_cutoff=80
        )

        if result:
            result = title_cache.get(result[0])

        return main_cache.get(result)
