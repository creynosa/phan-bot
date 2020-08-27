import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.has_role('Phan')
    async def clear(self, ctx, num):
        await ctx.message.delete()

        channel = ctx.channel
        await channel.purge(limit=int(num))
        return
    
    @commands.command()
    @commands.has_role('Phan')
    async def emptyTempFiles(self, ctx, num):
        files = [
            'fractalembeds.toml',
            'fractalteams.toml',
            'fractalteamspecs.toml'
        ]

        for fileName in files:
            with open(fileName, 'w') as f:
                f.seek(0)
                f.truncate()

        msg = await ctx.send('Files emptied!')
        await msg.delete(delay=3)

        return

def setup(bot):
    bot.add_cog(Moderation(bot))