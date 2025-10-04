from __future__ import annotations

from typing import TYPE_CHECKING
from core.services import search

import discord
from discord.ext import commands
from discord.ext.commands import Context

if TYPE_CHECKING:
    from bot.hoshiko import Hoshiko


class AnimeCog(commands.Cog):
    def __init__(self, bot: Hoshiko):
        self.bot = bot

    @commands.command(name="anime")
    async def anime_command(self, ctx: Context, anime: str) -> None:
        await ctx.send(f"Searching for {anime}...")
        result = await search(anime)
        r = result["data"][0]
        
        embed = discord.Embed(title=r['title'], description=r['synopsis'])
        embed.set_thumbnail(url=r['images']['webp']['large_image_url'])
        embed.add_field(name="Type", value=r['type'])
        embed.add_field(name="Source", value=r['source'])
        embed.add_field(name="Episodes", value=r['episodes'])

        view = discord.ui.View()
        button = discord.ui.Button(style=discord.ButtonStyle.link, label="MAL Link", url=r['url'])
        view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
