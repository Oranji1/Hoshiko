from __future__ import annotations

from pathlib import Path
from typing import Literal

from msgspec import Struct, toml


def load_config(path: str | None = "config.toml") -> Config:
    return toml.decode(Path(path).read_bytes(), type=Config)


class LoggingConfig(Struct):
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class BotConfig(Struct):
    prefix: str
    token: str


class Config(Struct):
    logging: LoggingConfig
    bot: BotConfig
