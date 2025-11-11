from __future__ import annotations

from pathlib import Path
from typing import Annotated, Literal

from msgspec import Meta, Struct, toml


def load_config(path: str | None = "config.toml") -> Config:
    return toml.decode(Path(path).read_bytes(), type=Config)


class LoggingConfig(Struct):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    file_max_mib: Annotated[int, Meta(ge=0)]
    file_backup_count: Annotated[int, Meta(ge=0)]


class BotConfig(Struct):
    prefix: str
    token: str


class Config(Struct):
    logging: LoggingConfig
    bot: BotConfig
