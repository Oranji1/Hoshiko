import json
from logging import getLevelName
from pathlib import Path

from bot.hoshiko import Hoshiko
from core.utils import setup_logger

with Path(f"{Path.cwd()}/config.json").open(encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["bot"]["token"]

try:
    import uvloop
except ModuleNotFoundError:
    import asyncio

    RUNTIME = asyncio.run
else:
    RUNTIME = uvloop.run


async def main() -> None:
    setup_logger(getLevelName(config["logging_level"]))

    async with Hoshiko(config) as bot:
        await bot.start(TOKEN, reconnect=True)


if __name__ == "__main__":
    RUNTIME(main())
