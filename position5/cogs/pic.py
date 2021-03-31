import discord
from discord.ext import commands
from . import delete_message, log_params, PIC_PATH


class Pic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='xdoubt', description='xdoubt pic')
    @delete_message()
    @log_params()
    async def xdoubt_command(self, ctx):
        await ctx.send(file=discord.File(f'{PIC_PATH}xdoubt.png'))


def setup(bot):
    bot.add_cog(Pic(bot))
