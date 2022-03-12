import os
import uuid
import discord
from discord.ext import commands
import boto3
from . import delete_message, log_params, FFMPEG_OPTIONS


class TTS(commands.Cog):
    "TTS Related commands"

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.polly_client = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name="eu-west-2",
        ).client("polly")

    @commands.command(name="tts", description="TTS in Brian voice")
    @delete_message()
    @log_params()
    async def brian_tts(self, ctx: commands.Context, *, text: str):
        response = self.polly_client.synthesize_speech(
            VoiceId="Brian", OutputFormat="mp3", Text=text, Engine="standard"
        )
        speech_id = uuid.uuid4()
        filename = "assets/tmp/speech_" + speech_id.hex + ".mp3"
        with open(filename, "wb") as file:
            file.write(response["AudioStream"].read())
        ctx.guild.voice_client.play(
            discord.FFmpegPCMAudio(source=filename, **FFMPEG_OPTIONS),
            after=lambda e: print(f"Player error: {e}") if e else None,
        )


def setup(bot):
    bot.add_cog(TTS(bot))
