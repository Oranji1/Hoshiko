import json
import os
from pathlib import Path

import discord
import jishaku
from discord.ext import commands

from core.cache import CacheManager

with Path(f"{Path.cwd()}/config.json").open(encoding="utf-8") as file:
    config = json.load(file)

TOKEN = config["bot"]["token"]

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


class Hoshiko(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="h!",
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.cm = CacheManager()

    async def load_cogs(self) -> None:
        for file in Path.iterdir(f"{os.path.realpath(Path(__file__).parent)}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                await self.load_extension(f"bot.cogs.{extension}")
                print(f"Loaded extension '{extension}'")  # noqa: T201 # I'll properly handle this later

    async def setup_hook(self) -> None:
        await self.load_extension("jishaku")
        await self.load_cogs()

    async def start(self) -> None:
        await super().start(token=self.config["bot"]["token"], reconnect=True)
