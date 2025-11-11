from logging import getLevelName

from bot.hoshiko import Hoshiko
from core.config import load_config
from core.utils import setup_logger

try:
    import uvloop
except ModuleNotFoundError:
    import asyncio

    RUNTIME = asyncio.run
else:
    RUNTIME = uvloop.run


async def main() -> None:
    config = load_config("config.toml")
    setup_logger(
        level=getLevelName(config.logging.level),
        max_mib=config.logging.file_max_mib,
        backup_count=config.logging.file_backup_count,
    )

    async with Hoshiko(config) as bot:
        await bot.start(config.bot.token, reconnect=True)


if __name__ == "__main__":
    RUNTIME(main())
