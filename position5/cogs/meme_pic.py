from os import listdir
from os.path import isfile, join
import random
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
        description='sends list of emotes'
    )
    async def emotes_command(self, ctx):
        await ctx.message.delete()
        embed_msg = discord.Embed(
            title='Available emotes:',
            description='\n'.join(['➥ ' + emote.split('.')[0] for emote in self.emotes]),
            color=random.choice(self.color_list)
        )
        await ctx.send(embed=embed_msg)
        return


def setup(bot):
    bot.add_cog(MemePic(bot))
