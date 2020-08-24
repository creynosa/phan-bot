import discord
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embedMessage(string):
        if string.startswith('http'):
            embed = discord.Embed(color=0x01a8ef)
            embed.set_image(url=string)
        else:
            embed = discord.Embed(description=string, color=0x01a8ef)
        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 293589451815387146:
            msg = message.content.lower()
            if 'fractal' in msg and 'god' in msg:
                await message.channel.send('<a:yapp:745690994661523519>')
        else:
            return


    @commands.command()
    async def caprikachu(self, ctx):
        embed = Fun.embedMessage('https://i.imgur.com/aqe7pfU.png')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def thanoscat(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/z2RtWzN.jpg")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))