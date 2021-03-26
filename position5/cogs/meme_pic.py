from os.path import isfile, getmtime
from pathlib import Path
from discord.ext import commands
import discord
from . import EMOTES_PATH


class MemePic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._refresh_emotes()

    def _refresh_emotes(self):
        self.emotes = [
            f.name
            for f in sorted(Path(EMOTES_PATH).iterdir(), key=getmtime)
            if isfile(f)
        ]
        self.emotes_dict = {
            emote.split('.', 1)[0].lower(): emote for emote in self.emotes
        }

    @commands.command(name='xdoubt', description='xdoubt pic')
    async def xdoubt_command(self, ctx):
        await ctx.message.delete()
        await ctx.send(file=discord.File('assets/meme_pic/xdoubt.png'))
        return

    @commands.command(name='emote', description='emote as pictures', usage='<emote>')
    async def emote_command(self, ctx, *, emote_name: str):
        await ctx.message.delete()
        if emote_name.lower() in self.emotes_dict:
            await ctx.send(
                file=discord.File(EMOTES_PATH + self.emotes_dict[emote_name.lower()])
            )
        return

    @commands.command(name='refresh', description='refresh emotes list')
    async def refresh_emotes(self, ctx):
        await ctx.message.delete()
        self._refresh_emotes()
        return

    @commands.command(
        name='emotes', description='sends list of emotes', usage='<search_string>'
    )
    async def emotes_command(self, ctx, *, search: str = None):
        await ctx.message.delete()
        title = f'Available emotes{f"({search})" if search else ""}:'
        emotes_list = []
        desc_list = []
        if search:
            for emote in self.emotes:
                if search.lower() in emote.lower():
                    emotes_list.append(emote.split('.')[0])
        else:
            emotes_list = [emote.split('.')[0] for emote in self.emotes]

        description = ''
        for emote in emotes_list:
            if len(description) >= 1900:
                desc_list.append(description)
                description = ''
            else:
                description += f'\n➥ {emote}'
        if description != '':
            desc_list.append(description)

        total_count = len(desc_list)
        for count, desc in enumerate(desc_list, 1):
            await ctx.send(
                embed=discord.Embed(
                    title=f'{title} [{count}/{total_count}]',
                    description=desc,
                    color=discord.Color.random(),
                )
            )

        if total_count == 0:
            await ctx.send(
                embed=discord.Embed(
                    title=title,
                    description='No emotes found',
                    color=discord.Color.random(),
                )
            )
        return


def setup(bot):
    bot.add_cog(MemePic(bot))
