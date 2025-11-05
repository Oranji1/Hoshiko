import logging
import os
from pathlib import Path

import discord
import jishaku
from discord.ext import commands

from core import CacheManager

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

logger = logging.getLogger(__name__)


class Hoshiko(commands.Bot):
    def __init__(self, config: dict) -> None:
        super().__init__(
            command_prefix=config["bot"]["prefix"],
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.cm = CacheManager()

    async def load_cogs(self) -> None:
        for file in os.listdir(f"{os.path.realpath(Path(__file__).parent)}/cogs"):  # noqa: PTH208
            if file.endswith(".py"):
                extension = file[:-3]
                await self.load_extension(f"bot.cogs.{extension}")
                logger.info("Loaded extension '%s'", extension)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_cogs()

    async def start(self, token: str, *, reconnect: bool = True) -> None:
        await super().start(token, reconnect=reconnect)
