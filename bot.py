import os
from discord.ext import commands

# Main Bot Token
TOKEN = os.environ['only-phans-bot-token']
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    """Print a console message when the bot is ready and active."""
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# Loads all cogs when ready
for filename in os.listdir('cogs'):
    if filename.endswith('.py') and filename != '__init__.py':
        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


# Initialize the Bot
bot.run(TOKEN)
