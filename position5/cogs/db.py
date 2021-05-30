from discord.ext import commands
from tinydb import TinyDB, Query
from . import delete_message, log_params


class Db(commands.Cog):
    """Fetch and store value in database"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.t_db = TinyDB("assets/db/db.json")
        self.query = Query()

    @commands.command(name="store", description="saves key value pair in database", aliases=["save"])
    @delete_message()
    @log_params()
    async def store_data(self, ctx: commands.Context, key: str, *, value: str):
        self.t_db.upsert(
            {"author": ctx.author.id, key: value},
            (self.query[key].exists()) & (self.query.author == ctx.author.id),
        )

    @commands.command(name="get", description="fetches value from database", aliases=["fetch"])
    @delete_message()
    @log_params()
    async def get_data(self, ctx: commands.Context, key: str):
        result = self.t_db.get((self.query[key].exists()) & (self.query.author == ctx.author.id))
        await ctx.send(result and f"Found - {key} : {result[key]}" or "Value not found")


def setup(bot):
    bot.add_cog(Db(bot))
