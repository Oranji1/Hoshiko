from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import discord
from discord.ext import commands

from core.services import search_anime

if TYPE_CHECKING:
    from discord.ext.commands import Context

    from bot.hoshiko import Hoshiko
    from core.structs import Anime


class AnimeCog(commands.Cog):
    def __init__(self, bot: Hoshiko) -> None:
        self.bot = bot

    @commands.command(name="anime")
    async def anime_command(
        self, ctx: Context, dont_check_cached: Literal["--no-cache"] | None = None, *, query: str
    ) -> None:
        embed = discord.Embed(
            description=f"Searching for {query}...", color=discord.Color.light_gray()
        )
        msg = await ctx.reply(embed=embed, mention_author=False)

        check_cached = not dont_check_cached
        anime: Anime = await search_anime(query, check_cached=check_cached, cache=self.bot.cm)

        if not anime:
            embed.description = "Oops! I couldn't find that anime..."
            embed.color = discord.Color.brand_red()
            await msg.edit(embed=embed)
            return

        embed.title = anime.title
        embed.description = anime.synopsis
        embed.set_thumbnail(url=anime.cover_url)
        embed.add_field(name="Type", value=anime.type)
        embed.add_field(name="Episodes", value=anime.episodes)
        embed.add_field(name="Source", value=anime.source)

        view = discord.ui.View()
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="AniList",
                url=anime.sites_urls.anilist,
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="MAL",
                url=anime.sites_urls.mal,
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ADB",
                url=anime.sites_urls.anidb,
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="ANN",
                url=anime.sites_urls.ann,
            ),
        ]

        for button in buttons:
            view.add_item(button)

        await msg.edit(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AnimeCog(client))
