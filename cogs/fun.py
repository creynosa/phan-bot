# A module containing various fun and simple commands for discord.

import discord
import re
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def embedMessage(string):
        """Returns a simple embed containing text or a picture.

        PARAMTERS
        string (str): text or an url to be displayed in an embed."""
        # If the user inputs an URL, the embed will only have the picture
        # displayed.
        if string.startswith("http"):
            embed = discord.Embed(color=0xFFFFFF)
            embed.set_image(url=string)
        # Anything else will generate a basic embed with text.
        else:
            embed = discord.Embed(description=string, color=0xFFFFFF)

        return embed

    @commands.Cog.listener()
    async def on_message(self, message):
        """Executes certain code blocks when a message is sent."""
        # Change the message's content to lowercase for case insensitivity.
        msg = message.content.lower()

        # Fun messages sent when either Bagu or Eversong (two discord members)
        # send a message with the phrase "Fractal God."
        if "fractal" in msg and "god" in msg:
            if message.author.id == eversongID:
                eversongID = 293589451815387146
                await message.channel.send("<a:yapp:745690994661523519>")
            elif message.author.id == baguID:
                baguID = 246875516387328000
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
        # choyaFilePath = "resources/images/choyabongo.gif"
        # with open(choyaFilePath, "rb") as f:
        #     discordFile = discord.File(f)

        embed = Fun.embedMessage("https://i.imgur.com/FJgfFTi.png")
        await ctx.send(embed=embed)

        # await ctx.send(file=discordFile)

    @commands.command()
    async def pusher(self, ctx):
        embed = Fun.embedMessage("https://i.imgur.com/0mHp2wx.png")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
