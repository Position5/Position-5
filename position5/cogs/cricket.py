import os
from discord.ext import commands
import discord
from cricapi import Cricapi
from . import delete_message, log_params


class Cricket(commands.Cog):
    """Cricket commands for now. Can be expanded to Sports if further developed"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.cricket_api = Cricapi(os.environ.get("CRIC_API"))

    @commands.command(name="cricket", description="cricket commands", aliases=["cric"])
    @delete_message()
    @log_params()
    async def cricket_scores(self, ctx: commands.Context):
        def check(msg):
            return msg.channel == ctx.message.channel and msg.author == ctx.message.author

        msg_og = await ctx.send(
            embed=discord.Embed(
                title="Fetching matches",
                color=discord.Color.random(),
            )
            .set_thumbnail(url=self.bot.user.avatar_url)
            .set_footer(
                text=f"Requested by {ctx.message.author.name}",
                icon_url=ctx.message.author.avatar_url,
            )
        )
        history = {}
        desc = ""
        matches = self.cricket_api.matches()["matches"]
        live_matches = [match for match in matches if match["matchStarted"]]
        for count, match in enumerate(live_matches, 1):
            desc += f"\n{count}. {match['team-1']} vs {match['team-2']}"
            history[str(count)] = match["unique_id"]
        desc += "\nReply with `<num>` for details"
        await msg_og.edit(
            embed=discord.Embed(
                title="Live cricket matches",
                description=desc[:2048],
                color=discord.Color.random(),
            )
        )

        msg = await self.bot.wait_for("message", check=check)
        reply = msg.content.strip()
        await msg.delete()

        if reply in history:
            scores = self.cricket_api.cricketScore({"unique_id": history[reply]})
            response = (
                discord.Embed(
                    title=scores["score"].replace("&amp;", "&") if "score" in scores else "Score not found",
                    color=discord.Color.random(),
                )
                .set_thumbnail(url=self.bot.user.avatar_url)
                .set_footer(
                    text=f"Requested by {ctx.message.author.name}",
                    icon_url=ctx.message.author.avatar_url,
                )
            )
            await msg_og.edit(embed=response)


def setup(bot):
    bot.add_cog(Cricket(bot))
