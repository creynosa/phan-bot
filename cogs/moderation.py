import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role("Phan")
    async def clear(self, ctx, num):
        await ctx.message.delete()

        channel = ctx.channel
        await channel.purge(limit=int(num))
        return


def setup(bot):
    bot.add_cog(Moderation(bot))