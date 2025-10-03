from __future__ import annotations
from discord.ext import commands
from discord.ext.commands import Context
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.hoshiko import Hoshiko

class AnimeCog(commands.Cog):
    def __init__(self, bot: Hoshiko):
        self.bot = bot

    @commands.command(name="anime")
    async def anime_command(self, ctx: Context, anime: str) -> None:
        await ctx.send(f"Searching for {anime}...")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
