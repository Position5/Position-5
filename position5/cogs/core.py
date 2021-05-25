from discord.ext import commands
from . import log_params, delete_message


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="logout")
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def close(self, ctx):
        await ctx.send("Logging off")
        await self.bot.close()


def setup(bot):
    bot.add_cog(Core(bot))
