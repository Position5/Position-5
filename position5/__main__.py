import os
from dotenv import load_dotenv
from discord.ext import commands
import replit
import keep_alive


load_dotenv('.env')


def get_prefix(client, message):
    # sets the prefixes, u can keep it as an array of only 1 item if you need only one prefix
    prefixes = ['.']

    if not message.guild:
        prefixes = ['==']   # Only allow '==' as a prefix when in DMs

    # Allow users to @mention the bot instead of using a prefix when using a command.
    return commands.when_mentioned_or(*prefixes)(client, message)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)


cogs = ['cogs.basic', 'cogs.embed', 'cogs.meme_pic']


@bot.event
async def on_ready():
    replit.clear()
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))
    bot.remove_command('help')
    for cog in cogs:
        bot.load_extension(cog)


keep_alive.keep_alive()

bot.run(os.getenv('DISCORD_BOT_TOKEN'), bot=True, reconnect=True)
