from os.path import isfile, getmtime
from pathlib import Path
import random
from discord.ext import commands
import discord
from . import COLORS as colors

EMOTES_PATH = 'assets/emotes/'


class MemePic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self._refresh_emotes()
        self.color_list = list(colors.values())

    def _refresh_emotes(self):
        self.emotes = [f.name for f in sorted(Path(EMOTES_PATH).iterdir(), key=getmtime) if isfile(f)]
        self.emotes_dict = {emote.split('.', 1)[0].lower(): emote for emote in self.emotes}

    @commands.command(
        name='xdoubt',
        description='xdoubt pic'
    )
    async def xdoubt_command(self, ctx):
        await ctx.message.delete()
        await ctx.send(file=discord.File('assets/meme_pic/xdoubt.png'))
        return

    @commands.command(
        name='emote',
        description='emote as pictures',
        usage='<emote>'
    )
    async def emote_command(self, ctx, *, emote_name: str):
        await ctx.message.delete()
        if emote_name.lower() in self.emotes_dict:
            await ctx.send(file=discord.File(EMOTES_PATH + self.emotes_dict[emote_name.lower()]))
        return

    @commands.command(
        name='refresh',
        description='refresh emotes list'
    )
    async def refresh_emotes(self, ctx):
        await ctx.message.delete()
        self._refresh_emotes()
        return

    @commands.command(
        name='emotes',
        description='sends list of emotes',
        usage='<search_string>'
    )
    async def emotes_command(self, ctx, *, search: str = None):
        await ctx.message.delete()
        title = f'Available emotes({search}):' if search else 'Available emotes:'
        description = ''
        embed_list = []
        search_not_found = True
        for emote in self.emotes:
            if search and search.lower() not in emote.lower():
                continue
            search_not_found = False
            description += '\n➥ ' + emote.split('.')[0]
            if len(description) > 1996:
                embed_list.append((title, description))
                description = ''
        if description != '':
            embed_list.append((title, description))

        total_count = len(embed_list)
        for count, (title, description) in enumerate(embed_list, 1):
            await ctx.send(embed=discord.Embed(
                title=f'{title} [{count}/{total_count}]',
                description=description,
                color=random.choice(self.color_list)
            ))

        # if no emotes found
        if description == '' and search and search_not_found:
            await ctx.send(embed=discord.Embed(
                title=title,
                description='No emotes found',
                color=random.choice(self.color_list)
            ))
        return


def setup(bot):
    bot.add_cog(MemePic(bot))
