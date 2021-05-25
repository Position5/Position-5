from datetime import datetime as dt
from discord.ext import commands
from . import delete_message, log_params


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ping', description='The ping command', aliases=['p'])
    @log_params()
    async def ping(self, ctx):
        start = dt.timestamp(dt.now())
        msg = await ctx.send(content='Pinging')

        await msg.edit(
            content=f'Pong!\nOne message round-trip took {(dt.timestamp(dt.now())-start) * 1000}ms.'
        )

    @commands.command(
        name='say',
        description='The say command',
        aliases=['repeat', 'parrot'],
        usage='<text>',
    )
    @delete_message()
    @log_params()
    async def say(self, ctx):
        msg = ctx.message.content
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used) :].strip()

        if text == '':
            await ctx.send(content='You need to specify the text!')
        else:
            await ctx.send(content=text)


def setup(bot):
    bot.add_cog(Basic(bot))
