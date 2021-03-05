from copy import deepcopy
from discord.ext import commands
import discord
from . import EMOJIS_DICT as emojis_dict


def char_to_emoji(char):
    if char.lower() in emojis_dict:
        return emojis_dict[char.lower()][0] + ' '
    return char


class React(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='alpha',
        description='say with alphabets',
        usage='<text>'
    )
    async def alpha_command(self, ctx, *, text):
        await ctx.message.delete()
        await ctx.send(content=(''.join([char_to_emoji(char) for char in text])))
        return

    @commands.command(
        name='avatar',
        description='get user avatar',
        aliases=['av'],
        usage='user'
    )
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        await ctx.message.delete()
        await ctx.send(avamember.avatar_url if avamember else ctx.author.avatar_url)
        return

    @commands.command(
        name='react',
        description='react to previous message with emoji',
        usage='-index(optional: <9) <emoji>',
        aliases=['re']
    )
    async def react_command(self, ctx, *, emoji: str = None):
        index = 1
        if emoji.startswith('-') and ' ' in emoji:
            _index, emoji = emoji.split(' ', 1)
            _index = _index[1:]
            if _index.isdigit():
                index = min(9, int(_index))

        last_message = await ctx.channel.history(limit=index + 1).flatten()
        await ctx.message.delete()
        await last_message[index].add_reaction(emoji)
        return

    @commands.command(
        name='clear',
        description='clear reactions from a message',
        usage='-index',
        aliases=['cls']
    )
    @commands.has_permissions(manage_messages=True)
    async def clear_reactions_command(self, ctx, *, index: int = 1):
        index = min(abs(index), 9)
        last_message = await ctx.channel.history(limit=index + 1).flatten()
        await ctx.message.delete()
        await last_message[index].clear_reactions()
        return

    @commands.command(
        name='previous',
        description='react to previous message with emojis(text)',
        usage='-index(optional: <9) <text>',
        aliases=['pre']
    )
    async def previous(self, ctx, *, text: str = None):
        index = 1
        if text.startswith('-') and ' ' in text:
            _index, text = text.split(' ', 1)
            _index = _index[1:]
            if _index.isdigit():
                index = min(9, int(_index))

        last_message = await ctx.channel.history(limit=index + 1).flatten()
        local_emojis = deepcopy(emojis_dict)
        await ctx.message.delete()

        for char in text.lower():
            if char in local_emojis and local_emojis[char]:
                await last_message[index].add_reaction(local_emojis[char].pop(0))
            elif char == ' ':
                continue
            else:
                break
        return


def setup(bot):
    bot.add_cog(React(bot))
