from msgspec import Struct


class BaseStruct(Struct, frozen=True, kw_only=True):
    pass
