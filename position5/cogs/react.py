from copy import deepcopy
from discord.ext import commands
import discord

emojis_dict = {
    'a': ['\U0001f1e6', '\U0001f170'], # jeans
    'b': ['\U0001f1e7', '\U0001f171'],
    'c': ['\U0001f1e8', '\U000000a9', '\U0001f318'],
    'd': ['\U0001f1e9'], # leftwards_arrow_with_hook
    'e': ['\U0001f1ea', '\U0001f4e7'],
    'f': ['\U0001f1eb'],
    'g': ['\U0001f1ec'], # compression
    'h': ['\U0001f1ed', '\U00002653'],
    'i': ['\U0001f1ee', '\U00002139'],
    'j': ['\U0001f1ef'],
    'k': ['\U0001f1f0'],
    'l': ['\U0001f1f1'],
    'm': ['\U0001f1f2', '\U000024c2', '\U0000264f'],
    'n': ['\U0001f1f3'],
    'o': ['\U0001f1f4', '\U0001f17e', '\U00002b55'], # record_button, doughnut, nazar_amulet
    'p': ['\U0001f1f5', '\U0001f17f'],
    'q': ['\U0001f1f6'],
    'r': ['\U0001f1f7', '\U000000ae'],
    's': ['\U0001f1f8', '\U0001f4b2'],
    't': ['\U0001f1f9'],
    'u': ['\U0001f1fa', '\U000026ce'],
    'v': ['\U0001f1fb'], # v, vs
    'w': ['\U0001f1fc'], # wc
    'x': ['\U0001f1fd', '\U0000274c', '\U0000274e', '\U00002716'],
    'y': ['\U0001f1fe'],
    'z': ['\U0001f1ff'],
    '0': ['0\U000020E3'],
    '1': ['1\U000020E3', '\U0001f947'],
    '2': ['2\U000020E3', '\U0001f948'],
    '3': ['3\U000020E3', '\U0001f949'],
    '4': ['4\U000020E3'],
    '5': ['5\U000020E3'],
    '6': ['6\U000020E3'],
    '7': ['7\U000020E3'],
    '8': ['8\U000020E3', '\U0001f3b1'],
    '9': ['9\U000020E3'],
}


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
        await ctx.send(avamember.avatar_url if avamember else self.bot.user.avatar_url)
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
