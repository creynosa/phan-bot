import os
import discord
from discord.ext import commands

# Enabling newly added discord intents.
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True

# Setting up the discord bot.
TOKEN = os.environ["phan-bot-token"]
bot = commands.Bot(command_prefix="*", intents=intents)


@bot.event
async def on_ready():
    """Print a console message when the bot is ready and active."""
    print("Embed Generator up!")
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


@bot.command()
async def update(ctx, embed_id):
    """Updates the text for an existing embed"""
    embedLogoURL = r"https://raw.githubusercontent.com/creynosa/phan-bot/main/resources/images/Phan%20Logo%20-%20135" \
                   r".png "

    originEmbed = await commands.MessageConverter().convert(ctx, embed_id)

    # newEmbed = discord.Embed(
    #     title="Guild Wars 2 Roles",
    #     description="""**React to sign up for the following roles**:

    #     <:fractals:784312868987338782> @fractals
    #     <:raids:784312867720921108> @raids
    #     <:strikes:784314456901550110> @strikes
    #     <:dungeons:784314457186631680> @dungeons
    #     <:guildmissions:798133880381112330> @guild missions""",
    #     color=0xFFFFFF,
    # )

    newEmbed = discord.Embed(
        title="#OnlyPhans Calendar (CST)",
        description="""**Monday**
        `Guild Missions` - 10:30 p.m.

        **Tuesday**
        N/A

        **Wednesday**
        `Wing 2` - 7:00 p.m.

        **Thursday**
        `Wing 3` - 7:00 p.m.

        **Friday**
        `Wings 1 + 4` - 7:00 p.m.

        **Saturday**
        `Wing 5` - 4:00 p.m.
        `Tabletop Night` - 10:30 p.m.

        **Sunday**
        `Wings 6 and 7` - 4:00 p.m.""",
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
