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
    config = load_config()
    setup_logger(getLevelName(config.logging.level))

    async with Hoshiko(config) as bot:
        await bot.start(config.bot.token, reconnect=True)


if __name__ == "__main__":
    RUNTIME(main())
