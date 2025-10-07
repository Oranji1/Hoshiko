from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.ext.commands import Context

from core.services import search

if TYPE_CHECKING:
    from bot.hoshiko import Hoshiko


class AnimeCog(commands.Cog):
    def __init__(self, bot: Hoshiko):
        self.bot = bot

    @commands.command(name="anime")
    async def anime_command(self, ctx: Context, *, anime: str) -> None:
        await ctx.send(f"Searching for {anime}...")
        anime = await search(anime)

        embed = discord.Embed(
            title=anime["title"]["romaji"], description=anime["synopsis"]
        )
        embed.set_thumbnail(url=anime["coverImage"]["large"])
        embed.add_field(name="Type", value=anime["format"])
        embed.add_field(name="Episodes", value=anime["episodes"])
        embed.add_field(name="Source", value=anime["source"])

        view = discord.ui.View()
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.link, label="AniList", url=anime["siteUrl"]
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="MAL",
                url=anime["extra_urls"]["mal"],
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ADB",
                url=anime["extra_urls"]["anidb"],
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ANN",
                url=anime["extra_urls"]["ann"],
            ),
        ]

        for button in buttons:
            view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
