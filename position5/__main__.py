import os
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv('.env')
bot = commands.Bot(command_prefix='.')


@bot.event
async def on_ready():
    print('Connected to bot: {}'.format(bot.user.name))
    print('Bot ID: {}'.format(bot.user.id))


@bot.command()
async def helloworld(ctx):
    await ctx.send('Allo World!')

bot.run(os.getenv('DISCORD_BOT_TOKEN'))
