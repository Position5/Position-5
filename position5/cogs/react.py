from copy import deepcopy
from discord.ext import commands
import discord
from . import EMOJIS_DICT, delete_message, log_params


def char_to_emoji(char):
    if char.lower() in EMOJIS_DICT:
        return EMOJIS_DICT[char.lower()][0] + " "
    return char


class React(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="alpha", description="say with alphabets", usage="<text>")
    @delete_message()
    @log_params()
    async def text_to_alpha_emotes(self, ctx, *, text):
        await ctx.send(content=("".join([char_to_emoji(char) for char in text])))

    @commands.command(name="avatar", description="get user avatar", aliases=["av"], usage="user")
    @delete_message()
    @log_params()
    async def user_avatar(self, ctx, *, avamember: discord.Member = None):
        await ctx.send(avamember.avatar_url if avamember else ctx.author.avatar_url)

    @commands.command(
        name="react",
        description="react to previous message with emoji",
        usage="-index(optional: <9) <emoji>",
        aliases=["re"],
    )
    @delete_message()
    @log_params()
    async def react_with_emote(self, ctx, *, emoji: str = None):
        index = 0
        if emoji.startswith("-") and " " in emoji:
            _index, emoji = emoji.split(" ", 1)
            _index = _index[1:]
            if _index.isdigit():
                index = min(9, int(_index))

        last_message = await ctx.channel.history(limit=index + 1).flatten()
        await last_message[index].add_reaction(emoji)

    @commands.command(
        name="clear",
        description="clear reactions from a message",
        usage="-index",
        aliases=["cls"],
    )
    @commands.has_permissions(manage_messages=True)
    @delete_message()
    @log_params()
    async def clear_reactions(self, ctx, *, index: int = 0):
        index = min(abs(index), 9)
        last_message = await ctx.channel.history(limit=index + 1).flatten()
        await last_message[index].clear_reactions()

    @commands.command(
        name="previous",
        description="react to previous message with emojis(text)",
        usage="-index(optional: <9) <text>",
        aliases=["pre"],
    )
    @delete_message()
    @log_params()
    async def react_to_previous(self, ctx, *, text: str = None):
        index = 0
        if text.startswith("-") and " " in text:
            _index, text = text.split(" ", 1)
            _index = _index[1:]
            if _index.isdigit():
                index = min(9, int(_index))

        last_message = await ctx.channel.history(limit=index + 1).flatten()
        local_emojis = deepcopy(EMOJIS_DICT)

        for char in text.lower():
            if char in local_emojis and local_emojis[char]:
                await last_message[index].add_reaction(local_emojis[char].pop(0))
            elif char == " ":
                continue
            else:
                break


def setup(bot):
    bot.add_cog(React(bot))
