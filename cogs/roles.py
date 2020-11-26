import discord
import configparser
from discord.ext import commands


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roleEmbed(self, ctx):
        """Starts the process of creating, deleting, or updating a role embed."""

        initialEmbed = discord.Embed(
            title="Role Embed Options",
            color=0xFFFFFF,
        )
        initialEmbed.add_field(
            name="Please select one of the following by entering the corresponding number:",
            value="""`1.` Create a new role embed
            `2.` Update an existing role embed
            `3.` Delete an existing role embed""",
        )

        await ctx.send(embed=initialEmbed)


def setup(bot):
    bot.add_cog(Roles(bot))