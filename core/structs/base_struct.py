from msgspec import Struct, field, structs

from core.errors import URLValidationError
from core.utils import http_url_validator

from .enums import MediaType


class BaseStruct(Struct, frozen=True):
    pass


class BaseMediaStruct(BaseStruct, kw_only=True):
    title: str
    synopsis: str | None = "N/A"
    cover_url: str | None = None
    type: MediaType
    titles: list[dict[str, str]] | None = field(default_factory=list)

    def __post_init__(self) -> None:
        cover_url = self.cover_url

        if not cover_url:
            pass
        try:
            http_url_validator(cover_url, allowed_host="cdn.myanimelist.net")
        except URLValidationError:
            structs.force_setattr(self, "cover_url", None)
