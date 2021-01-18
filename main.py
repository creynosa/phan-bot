import os
import discord
from discord.ext import commands

# Enabling newly added discord intents.
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.reactions = True
intents.messages = True

# Setting up the discord bot.
TOKEN = os.environ["phan-bot-token"]
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Print a console message when the bot is ready and active."""
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")

    # Loads all the included cogs when ready.
    for filename in os.listdir("cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            bot.load_extension(f"cogs.{filename[:-3]}")


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


# Initialize the Bot
if __name__ == "__main__":
    bot.run(TOKEN)
