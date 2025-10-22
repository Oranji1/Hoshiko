from __future__ import annotations

from typing import TYPE_CHECKING

import discord
from discord.ext import commands

from core.services import search_manga

if TYPE_CHECKING:
    from discord.ext.commands import Context

    from bot.hoshiko import Hoshiko
    from core.models import Manga


class MangaCog(commands.Cog):
    def __init__(self, bot: Hoshiko) -> None:
        self.bot = bot

    @commands.command(name="manga")
    async def manga_command(self, ctx: Context, *, query: str) -> None:
        await ctx.send(f"Searching for {query}...")
        manga: Manga = await search_manga(query, self.bot.cm)

        if not manga:
            await ctx.send("Oops! I couldn't find that manga...")
            return

        embed = discord.Embed(title=manga.title, description=manga.synopsis)
        embed.set_thumbnail(url=manga.cover_url)
        embed.add_field(name="Type", value=manga.type)
        embed.add_field(name="Chapters", value=manga.chapters)
        embed.add_field(name="Volumes", value=manga.volumes)

        view = discord.ui.View()
        buttons = [
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="AniList",
                url=manga.sites_urls.anilist.encoded_string(),
            ),
            discord.ui.Button(
                style=discord.ButtonStyle.link,
                label="MAL",
                url=manga.sites_urls.mal.encoded_string(),
            ),
        ]

        for button in buttons:
            view.add_item(button)

        await ctx.send(embed=embed, view=view)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(MangaCog(client))
