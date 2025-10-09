from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands
from discord.ext.commands import Context

from core.services import search

if TYPE_CHECKING:
    from bot.hoshiko import Hoshiko
    from core.models.anime import Anime


class AnimeCog(commands.Cog):
    def __init__(self, bot: Hoshiko):
        self.bot = bot

    @commands.command(name="anime")
    async def anime_command(self, ctx: Context, *, anime: str) -> None:
        await ctx.send(f"Searching for {anime}...")
        anime: Anime = await search(anime)

        embed = discord.Embed(title=anime.title, description=anime.synopsis)
        embed.set_thumbnail(url=anime.cover_url)
        embed.add_field(name="Type", value=anime.type)
        embed.add_field(name="Episodes", value=anime.episodes)
        embed.add_field(name="Source", value=anime.source)

        view = discord.ui.View()
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="AniList",
                url=anime.sites_urls.anilist.encoded_string(),
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="MAL",
                url=anime.sites_urls.mal.encoded_string(),
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ADB",
                url=anime.sites_urls.anidb.encoded_string(),
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ANN",
                url=anime.sites_urls.ann.encoded_string(),
            ),
        ]

        for button in buttons:
            view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
