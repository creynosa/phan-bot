# A module containing various commands to be used only by the
# discord server owner.

import discord
import datetime
import pytz
from discord.ext import commands

# Setting a timezone for use with timestamps.
localTZ = pytz.timezone("US/Central")


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        # Check to see if the user is a moderator.
        isOwner = await self.bot.is_owner(ctx.author)
        return isOwner

    @commands.command()
    async def clear(self, ctx, num):
        """Deletes a set number of messages in a specific channel.

        PARAMETERS
        num (str): the number of messages to delete"""

        # Delete the original "!clear" command used to execute this block.
        await ctx.message.delete()

        # COMMENCE THE PURGE!!
        channel = ctx.channel
        await channel.purge(limit=int(num))
        return

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """Executes certain code when a message is deleted."""
        # Set the channel used for notifications.
        targetChannelID = 800578740484440114
        targetChannel = self.bot.get_channel(targetChannelID)

        # Retrieve information from the deleted message.
        author = message.author
        authorPFPUrl = author.avatar_url
        content = message.content
        channel = message.channel
        timeCreated = message.created_at.replace(tzinfo=pytz.utc)

        # (OPTIONAL)
        timeCreatedCST = timeCreated.astimezone(localTZ).strftime(
            "%m/%d/%y at %I:%M %p %Z"
        )

        # Create the embed containing the message's information.
        newEmbed = discord.Embed(
            title=f"Looks like a message was deleted in #{channel}!",
            description=f"{content}",
            color=0xFFFFFF,
        )
        newEmbed.set_thumbnail(url=authorPFPUrl)
        newEmbed.set_author(name=author, icon_url=authorPFPUrl)
        newEmbed.set_footer(text=f"Deleted message was created on {timeCreatedCST}")

        # Send the embed to the indicated channel.
        await targetChannel.send(embed=newEmbed)

        return


def setup(bot):
    bot.add_cog(Moderation(bot))