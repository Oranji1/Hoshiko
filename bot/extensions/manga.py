from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import discord
from discord.ext import commands

from core.services import MangaService

if TYPE_CHECKING:
    from discord.ext.commands import Context

    from bot.hoshiko import Hoshiko


class MangaCog(commands.Cog):
    def __init__(self, bot: Hoshiko) -> None:
        self.bot = bot
        self.service = MangaService(bot.cm)

    @commands.command(name="manga")
    async def manga_command(
        self, ctx: Context, dont_check_cached: Literal["--no-cache"] | None = None, *, query: str
    ) -> None:
        embed = discord.Embed(
            description=f"Searching for {query}...", color=discord.Color.light_gray()
        )
        msg = await ctx.reply(embed=embed, mention_author=False)

        check_cached = not dont_check_cached
        manga = await self.service.search(query, check_cached=check_cached)

        if not manga:
            embed.description = "Oops! I couldn't find that manga..."
            embed.color = discord.Color.brand_red()
            await msg.edit(embed=embed)
            return

        embed.title = manga.title
        embed.description = manga.synopsis
        embed.set_thumbnail(url=manga.cover_url)
        embed.add_field(name="Type", value=manga.type)
        embed.add_field(name="Chapters", value=manga.chapters)
        embed.add_field(name="Volumes", value=manga.volumes)

        view = discord.ui.View()
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="AniList",
                url=manga.sites_urls.anilist,
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="MAL",
                url=manga.sites_urls.mal,
            ),
        ]

        for button in buttons:
            view.add_item(button)

        await msg.edit(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MangaCog(client))
