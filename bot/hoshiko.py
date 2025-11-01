import json
import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

import discord
import jishaku
from discord.ext import commands

from core import CacheManager

with Path(f"{Path.cwd()}/config.json").open(encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["bot"]["token"]
LOG_DIR = Path("./logs/")
LOG_DIR.mkdir(exist_ok=True)

intents = discord.Intents().default()
intents.message_content = True
intents.bans = False
intents.auto_moderation = False
intents.typing = False
intents.expressions = False
intents.voice_states = False
intents.invites = False
intents.moderation = False
intents.members = True
intents.reactions = False

jishaku.Flags.NO_DM_TRACEBACK = True
jishaku.Flags.NO_UNDERSCORE = True


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("hoshiko")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "[{asctime}] [{levelname}] {name}: {message}", "%Y-%m-%d %H:%M:%S", style="{"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        LOG_DIR / "hoshiko.log", maxBytes=32 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


class Hoshiko(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=config["bot"]["prefix"],
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.cm = CacheManager()
        self.logger = setup_logger()

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(Path(__file__).parent)}/cogs"):  # noqa: PTH208
            if file.endswith(".py"):
                extension = file[:-3]
                await self.load_extension(f"bot.cogs.{extension}")
                self.logger.info("Loaded extension '%s'", extension)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_cogs()

    async def start(self) -> None:
        await super().start(token=self.config["bot"]["token"], reconnect=True)
