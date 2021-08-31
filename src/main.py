import discord
from discord.ext import commands

from config import discord_secret, extensions, prefix

intents = discord.Intents.default()
intents.members = True
intents.messages = True
bot = commands.Bot(command_prefix=prefix, description="Revision server bot", intents=intents, case_insensitive=True)


@bot.event 
async def on_ready():
    print("--------")
    print(f"Logged in as {bot.user.name} - {bot.user.id}")
    print("--------")

    print("Loading cogs...")
    for file in extensions:
        bot.load_extension(f"cogs.{file}")
        print(f"Loaded cogs.{file}")
    print("--------")


bot.run(discord_secret)
