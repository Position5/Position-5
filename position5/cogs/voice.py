import logging
from discord.ext import commands
import discord
from . import delete_message, log_params

log = logging.getLogger("position5.cogs.voice")


class Voice(commands.Cog):
    "Voice channel related commands"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="join", description="joins voice channel")
    @delete_message()
    @log_params()
    async def join_voice_channel(self, ctx: commands.Context):
        voice = ctx.author.voice
        if not voice:
            await ctx.send("Please join a voice channel")
            return
        channel = voice.channel
        await channel.connect()

    @join_voice_channel.error
    async def join_voice_channel_handler(self, ctx: commands.Context, error):
        error = getattr(error, "original", error)
        if isinstance(error, discord.ClientException):
            await ctx.send(str(error))
        else:
            log.info("Exception in command %s", ctx.command)
            log.error("Type %s | Error: %s", type(error), error)
            raise error

    @commands.command(name="move", description="move to current voice channel")
    @delete_message()
    @log_params()
    async def move_to_voice_channel(self, ctx: commands.Context):
        voice = ctx.author.voice
        if not voice:
            await ctx.send("You're not in a voice channel")
            return
        voice_client = ctx.voice_client
        await voice_client.move_to(voice.channel)

    @commands.command(name="leave", description="leaves voice channel")
    @delete_message()
    @log_params()
    async def leave_voice_channel(self, ctx: commands.Context):
        voice = ctx.author.voice
        if not voice:
            await ctx.send("You're not in a voice channel")
            return
        voice_client = ctx.guild.voice_client
        await voice_client.disconnect()


def setup(bot):
    bot.add_cog(Voice(bot))
