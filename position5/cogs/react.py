from discord.ext import commands
import discord


digit_to_string = {
    1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
    6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 0: 'zero'
}

char_to_emojis = {
    'a': ['regional_indicator_a', 'a'], # jeans
    'b': ['regional_indicator_b', 'b'],
    'c': ['regional_indicator_c', 'copyright', 'waning_crescent_moon'],
    'd': ['regional_indicator_d'], # leftwards_arrow_with_hook
    'e': ['regional_indicator_e'], # email
    'f': ['regional_indicator_f'],
    'g': ['regional_indicator_g'], # compression
    'h': ['regional_indicator_h'],
    'i': ['regional_indicator_i', 'information_source'],
    'j': ['regional_indicator_j'],
    'k': ['regional_indicator_k'],
    'l': ['regional_indicator_l'],
    'm': ['regional_indicator_m', 'm'],
    'n': ['regional_indicator_n'],
    'o': ['regional_indicator_o', 'o2', 'o', 'record_button'], # doughnut, nazar_amulet
    'p': ['regional_indicator_p', 'parking'],
    'q': ['regional_indicator_q'],
    'r': ['regional_indicator_r', 'registered'],
    's': ['regional_indicator_s', 'heavy_dollar_sign'],
    't': ['regional_indicator_t'],
    'u': ['regional_indicator_u', 'ophiuchus'],
    'v': ['regional_indicator_v'], # v, vs
    'w': ['regional_indicator_w'], # wc
    'x': ['regional_indicator_x', 'x', 'negative_squared_cross_mark', 'heavy_multiplication_x'],
    'y': ['regional_indicator_y'],
    'z': ['regional_indicator_z'],
    '0': ['zero'],
    '1': ['one', 'first_place'],
    '2': ['two', 'second_place'],
    '3': ['three', 'third_place'],
    '4': ['four'],
    '5': ['five'],
    '6': ['six'],
    '7': ['seven'],
    '8': ['eight', '8ball'],
    '9': ['nine'],
}


def char_to_emoji(char):
    if char.isalpha():
        return f':regional_indicator_{char.lower()}: '
    if char.isdigit():
        return f':{digit_to_string[int(char)]}: '
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
        await ctx.send(content=''.join([char_to_emoji(char) for char in text]))
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
        usage='<emoji>',
        aliases=['re']
    )
    async def react_command(self, ctx, *, emoji: str = None):
        last_message = await ctx.channel.history(limit=2).flatten()
        await ctx.message.delete()
        await last_message[-1].add_reaction(emoji)
        return

    @commands.command(
        name='previous',
        description='react to previous message with emojis(text)',
        usage='<text>',
        aliases=['pre']
    )
    async def previous(self, ctx, *, text: str = None):
        # last_message = await ctx.channel.history(limit=2).flatten()
        await ctx.message.delete()
        print(text)
        return


def setup(bot):
    bot.add_cog(React(bot))
