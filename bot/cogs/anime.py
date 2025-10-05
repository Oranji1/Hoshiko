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
        result = await search(anime)
        r = result["data"]['Page']['media'][0]

        embed = discord.Embed(title=r["title"]['romaji'], description=r["description"])
        embed.set_thumbnail(url=r["coverImage"]["large"])
        embed.add_field(name="Type", value=r["format"])
        embed.add_field(name="Episodes", value=r["episodes"])
        embed.add_field(name="Source", value=r["source"])

        view = discord.ui.View()
        anilist_button = discord.ui.Button(
            style=discord.ButtonStyle.link, label="AniList", url=r["siteUrl"]
        )
        mal_button = discord.ui.Button(
            style=discord.ButtonStyle.link, label="MAL", url=r["extra_urls"]['mal']
        )
        view.add_item(anilist_button)
        view.add_item(mal_button)

        await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
