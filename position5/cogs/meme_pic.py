from os import listdir
from os.path import isfile, join
import random
import asyncio
from discord.ext import commands
import discord
from .embed import colors


class MemePic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emotes = [f for f in listdir('assets/emotes/') if isfile(join('assets/emotes/', f))]
        self.color_list = list(colors.values())

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
    async def emote_command(self, ctx, *, name):
        await ctx.message.delete()
        for emote in self.emotes:
            if name.lower() == emote.split('.', 1)[0].lower():
                await ctx.send(file=discord.File('assets/emotes/' + emote))
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
                embed_list.append(ctx.send(embed=discord.Embed(
                    title=title,
                    description=description,
                    color=random.choice(self.color_list)
                )))
                description = ''
        if description != '':
            embed_list.append(ctx.send(embed=discord.Embed(
                title=title,
                description=description,
                color=random.choice(self.color_list)
            )))
        for future in asyncio.as_completed(embed_list):
            await future
        if description == '' and search and search_not_found:
            await ctx.send(embed=discord.Embed(
                title=title,
                description='No emotes found',
                color=random.choice(self.color_list)
            ))
        return


def setup(bot):
    bot.add_cog(MemePic(bot))
