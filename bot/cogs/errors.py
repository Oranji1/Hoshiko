import discord
from discord import Color
from discord.ext import commands
from discord.ext.commands import Context

from core.errors import APIError, NotFoundError


class ErrorsCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception) -> None:  # noqa: PLR6301
        if isinstance(error, commands.CommandNotFound):
            return

        original = error.original
        error_embed = discord.Embed(color=Color.brand_red())

        if isinstance(error, commands.BotMissingPermissions):
            error_embed.description = f"I'm missing `{error.missing_permissions}` permission to execute that command correctly!"  # noqa: E501 # I'll properly handle this linter error once I add a translation system
            await ctx.reply(embed=error_embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = "It looks like you're forgetting to add some arguments!"
            await ctx.reply(embed=error_embed)
        elif isinstance(original, NotFoundError):
            error_embed.description = "I couldn't find that resource..."
            await ctx.reply(embed=error_embed)
        elif isinstance(original, APIError):
            error_embed.description = "Oops! There was an error trying to access that resource."
        else:
            error_embed.description = "Oops! Something went really wrong..."
            await ctx.reply(embed=error_embed)
            raise error


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ErrorsCog(bot))
