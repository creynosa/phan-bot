import discord
import re
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embedMessage(string):
        """Returns a simple colored embed for use with text or images."""
        if string.startswith("http"):
            embed = discord.Embed(color=0xFFFFFF)
            embed.set_image(url=string)
        else:
            embed = discord.Embed(description=string, color=0xFFFFFF)

        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        """Executes code blocks when certain messages are sent."""

        # Fun message responding to Eversong or Bagu saying "Fractal God."
        eversongID = 293589451815387146
        baguID = 246875516387328000

        msg = message.content.lower()
        if "fractal" in msg and "god" in msg:
            if message.author.id == eversongID:
                await message.channel.send("<a:yapp:745690994661523519>")
            elif message.author.id == baguID:
                baguEmbed = Fun.embedMessage("soon™")
                await message.channel.send(embed=baguEmbed)

    @commands.command()
    async def eversong(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/HijmLV8.jpg")
        await ctx.send(embed=embed)

    @commands.command()
    async def caprikachu(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/aqe7pfU.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def bagu4k(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/Wp9aJ4q.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def enter(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/tNSoLk5.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def thanoscat(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/z2RtWzN.jpg")
        await ctx.send(embed=embed)

    @commands.command()
    async def phan(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/7QYM7JB.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def marshiiee(self, ctx):
        marshiieID = 142809966749679616
        marshiieUser = await self.bot.fetch_user(marshiieID)

        embed = Fun.embedMessage("https://i.imgur.com/UgiwdJV.png")
        await ctx.send(
            f"Introducing: the <:ayaya:745792801215610930> Ayaya"
            f"{marshiieUser.mention} Collection™ <:ayaya:745792801215610930>",
            embed=embed,
        )

    @commands.command()
    async def maniicc(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/k94JJVU.png")
        await ctx.send(embed=embed)

    @commands.command()
    async def kat(self, ctx):
        choyaFilePath = "resources/images/choyabongo.gif"
        with open(choyaFilePath, "rb") as f:
            discordFile = discord.File(f)

        await ctx.send(file=discordFile)

    @commands.command()
    async def pusher(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/0mHp2wx.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))