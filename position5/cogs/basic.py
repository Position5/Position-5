from datetime import datetime as dt
import discord
from discord.ext import commands
from . import delete_message, log_params


class Basic(commands.Cog):
    """Totally basic commands, with no/simple logic"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping", description="The ping command", aliases=["p"])
    @log_params()
    async def ping(self, ctx: commands.Context):
        start = dt.timestamp(dt.now())
        msg = await ctx.send(content="Pinging")

        await msg.edit(
            content=f"Pong!\nOne message round-trip took {(dt.timestamp(dt.now())-start) * 1000}ms."
        )

    @commands.command(
        name="say",
        description="The say command",
        aliases=["repeat", "parrot"],
        usage="<text>",
    )
    @delete_message()
    @log_params()
    async def say(self, ctx: commands.Context):
        msg = ctx.message.content
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used) :].strip()

        if text == "":
            await ctx.send(content="You need to specify the text!")
        else:
            await ctx.send(content=text)

    @commands.command(name="dm", description="dm user", hidden=True)
    @commands.has_permissions(administrator=True)
    @delete_message()
    @log_params()
    async def send_dm(
        self, ctx: commands.Context, member: discord.Member, *, content: str
    ):
        channel = await member.create_dm()
        await channel.send(content)


def setup(bot):
    bot.add_cog(Basic(bot))
