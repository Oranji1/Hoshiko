from __future__ import annotations

import uuid
from typing import Any

from cachetools import LRUCache

from core.models.anime import Anime


def make_uuid() -> str:
    return str(uuid.uuid4())


class CacheManager:
    def __init__(self, maxsize: int = 512):
        class SyncedLRUCache(LRUCache):
            def __init__(self, parent: CacheManager, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self._parent = parent

            def popitem(self) -> tuple[Any, Any]:
                key, value = super().popitem()
                self._parent._remove_titles_for(key)
                return key, value

        self.main_cache = SyncedLRUCache(self, maxsize=maxsize)
        self.title_cache: dict[str, str] = {}

    def _remove_titles_for(self, identifier: str) -> None:
        to_remove = [k for k, v in self.title_cache.items() if v == identifier]
        for k in to_remove:
            del self.title_cache[k]

    def add(self, model: Anime) -> str:
        id = make_uuid()
        self.main_cache[id] = model.model_dump()

        for title in model.alt_titles.values():
            if title not in self.title_cache:
                self.title_cache[title.lower()] = id

        for synonym in model.synonyms:
            if synonym not in self.title_cache:
                self.title_cache[synonym.lower()] = id

        return id

    def get_by_id(self, id: str) -> Any | None:
        return self.main_cache.get(id)

    def get_by_title(self, title: str) -> Any | None:
        if id := self.title_cache.get(title.lower()):
            return self.main_cache.get(id)
        return None
