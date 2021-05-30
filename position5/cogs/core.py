from discord.ext import commands
from . import log_params, delete_message, COGS


class Core(commands.Cog):
    """Core commands for bot's operation/maintenance. Preferably for admins"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def _reload_cog(self, cog: str):
        try:
            self.bot.reload_extension(cog)
        except commands.ExtensionNotLoaded:
            self.bot.load_extension(cog)

    def _load_cog(self, cog: str):
        try:
            self.bot.load_extension(cog)
        except commands.ExtensionAlreadyLoaded:
            self.bot.reload_extension(cog)

    def _unload_cog(self, cog: str):
        try:
            self.bot.unload_extension(cog)
        except commands.ExtensionNotLoaded:
            pass

    @commands.command(name="logout", hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def close(self, ctx: commands.Context):
        await ctx.send("Logging off")
        await self.bot.close()

    @commands.command(name="unloadcog", aliases=["uc"], hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def unload_cog(self, ctx: commands.Context, cog_name: str):
        self._unload_cog(f"cogs.{cog_name}")

    @commands.command(name="loadcog", aliases=["lc"], hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def load_cog(self, ctx: commands.Context, cog_name: str):
        self._load_cog(f"cogs.{cog_name}")

    @commands.command(name="reloadcog", aliases=["rc"], hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def reload_cog(self, ctx: commands.Context, cog_name: str):
        self._reload_cog(f"cogs.{cog_name}")

    @commands.command(name="reload", hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def reload_all_cogs(self, ctx: commands.Context):
        for cog in COGS:
            self._reload_cog(cog)


def setup(bot):
    bot.add_cog(Core(bot))
