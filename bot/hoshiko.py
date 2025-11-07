import logging

import discord
import jishaku
from discord.ext import commands

from bot.extensions import EXTENSIONS
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

    async def load_extensions(self) -> None:
        for ext in EXTENSIONS:
            try:
                await self.load_extension(ext)
            except Exception:
                logger.exception("Failed to load extension '%s'", ext)
            else:
                logger.info("Loaded extension '%s'", ext)

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_extensions()
