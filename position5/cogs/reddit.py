import os
from discord.ext import commands
import asyncpraw
from . import delete_message, log_params


class Reddit(commands.Cog):
    """Reddit related commands"""

    def __init__(self, bot):
        self.bot = bot
        self.reddit = asyncpraw.Reddit(
            client_id=os.getenv("REDDIT_ID"),
            client_secret=os.getenv("REDDIT_SECRET"),
            user_agent="discord:position:5 (by u/appi147)",
        )

    @commands.command(name="chloe", description="get latest chloe")
    @delete_message()
    @log_params()
    async def get_chloe_latest(self, ctx):
        subreddit = await self.reddit.subreddit("chloe")
        async for submission in subreddit.new(limit=1):
            await ctx.send(submission.url)


def setup(bot):
    bot.add_cog(Reddit(bot))
