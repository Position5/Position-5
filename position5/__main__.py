import sys
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
import discord
from cogs import COGS


def get_prefix(client, message):
    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    prefixes = ["."]

    if not message.guild:
        prefixes = ["=="]  # Only allow '==' as a prefix when in DMs

    # Allow users to @mention the bot instead of using a prefix when using a command.
    return commands.when_mentioned_or(*prefixes)(client, message)


def setup_logging():
    file_handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
    file_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    dpy_logger = logging.getLogger("discord")
    dpy_logger.setLevel(logging.INFO)
    dpy_logger.addHandler(file_handler)

    position5_logger = logging.getLogger("position5")
    position5_logger.setLevel(logging.DEBUG)
    position5_logger.addHandler(stdout_handler)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents().all())


@bot.event
async def on_ready():
    print("Connected to bot: {}".format(bot.user.name))
    print("Bot ID: {}".format(bot.user.id))
    bot.remove_command("help")
    for cog in COGS:
        bot.load_extension(cog)


def start_bot():
    setup_logging()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"), bot=True, reconnect=True)


if __name__ == "__main__":
    load_dotenv(".env")
    start_bot()
