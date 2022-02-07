from os.path import isfile, getmtime
from pathlib import Path
from discord.ext import commands
import discord
from . import EMOTES_PATH, delete_message, log_params


class Emotes(commands.Cog):
    "Emotes commands"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._refresh_emotes()

    def _refresh_emotes(self):
        self.emotes = [
            f.name
            for f in sorted(Path(EMOTES_PATH).iterdir(), key=getmtime)
            if isfile(f)
        ]
        self.emotes_dict = {
            emote.split(".", 1)[0].lower(): emote for emote in self.emotes
        }

    @commands.command(name="emote", description="emote as pictures", usage="<emote>")
    @delete_message()
    @log_params()
    async def send_emote(self, ctx: commands.Context, *, emote_name: str):
        if emote_name.lower() in self.emotes_dict:
            await ctx.send(
                file=discord.File(EMOTES_PATH + self.emotes_dict[emote_name.lower()])
            )

    @commands.command(name="refe", description="refresh emotes list")
    @delete_message()
    @log_params()
    async def refresh_emotes(self, ctx: commands.Context):
        self._refresh_emotes()

    @commands.command(
        name="emotes", description="sends list of emotes", usage="<search_string>"
    )
    @delete_message()
    @log_params()
    async def list_emotes(self, ctx: commands.Context, *, search: str = None):
        title = f"Available emotes{f'({search})' if search else ''}:"
        emotes_list = []
        desc_list = []
        if search:
            for emote in self.emotes:
                if search.lower() in emote.lower():
                    emotes_list.append(emote.split(".")[0])
        else:
            emotes_list = [emote.split(".")[0] for emote in self.emotes]

        description = ""
        for emote in emotes_list:
            description += f"\n➥ {emote}"
            if len(description) >= 1900:
                desc_list.append(description)
                description = ""

        if description != "":
            desc_list.append(description)

        total_count = len(desc_list)
        if total_count == 0:
            await ctx.send(
                embed=discord.Embed(
                    title=title,
                    description="No emotes found",
                    color=discord.Color.random(),
                )
            )
            return

        for count, desc in enumerate(desc_list, 1):
            await ctx.send(
                embed=discord.Embed(
                    title=f"{title} [{count}/{total_count}]",
                    description=desc,
                    color=discord.Color.random(),
                )
            )


def setup(bot):
    bot.add_cog(Emotes(bot))
