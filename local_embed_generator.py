# For use on a local machine in order to edit, create, and delete embedded
# messages on the fly.

import os
import discord
from discord.ext import commands

# Establishing newly-added discord intents.
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

# Set up the discord bot with a different prefix than the original bot.
TOKEN = os.environ["phan-bot-token"]
bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():
    """Print a console message when the bot is ready and active."""
    print("Local client up!")
    print("------")


@bot.event
async def on_message(message):
    """Executes certain code blocks upon a message being sent."""

    # Ignore the bot's own messages.
    if message.author == bot.user:
        return

    # Ignore commands from working through DMs.
    if type(message.channel) == discord.DMChannel:
        return

    await bot.process_commands(message)


# Commands for use when needed to make immediate changes rather than pushing
# to a remote server constantly.
@bot.command()
async def update(ctx, embed_id):
    """Updates the text for an existing embed.

    PARAMETERS
    embed_id: the ID of the embedded message (str)

    RETURNS
    Nothing. Edits the original embedded message in realtime.
    """

    embedLogoURL = (
        r"https://raw.githubusercontent.com/creynosa/phan-bot/main/resources/images/Phan%20Logo%20-%20135"
        r".png "
    )

    # Retrieving the original embed via the user-inputted embed ID.
    originEmbed = await commands.MessageConverter().convert(ctx, embed_id)

    # Both the title and the text will need to be hardcoded in this section.
    # Could research adding a UI in the future to take raw input.
    embedTitle = "Guild Wars 2 Roles"

    embedText = """**React to sign up for the following roles**:

        <:fractals:784312868987338782> @fractals
        <:raids:784312867720921108> @raids
        <:strikes:784314456901550110> @strikes
        <:dungeons:784314457186631680> @dungeons
        <:guildmissions:798133880381112330> @guild missions"""

    newEmbed = discord.Embed(
        title=embedTitle,
        description=embedText,
        color=0xFFFFFF,
    )

    newEmbed.set_author(
        name="Phan Bot",
        icon_url=embedLogoURL,
    )

    await originEmbed.edit(embed=newEmbed)


# Initialize the Bot
if __name__ == "__main__":
    bot.run(TOKEN)
