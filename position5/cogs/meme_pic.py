from discord.ext import commands
import discord

class MemePic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(
        name='xdoubt',
        description='xdoubt pic'
    )
    async def xdoubt_command(self, ctx):
        await ctx.message.delete()
        await ctx.send(file=discord.File('assets/meme_pic/xdoubt.png'))
        return


def setup(bot):
    bot.add_cog(MemePic(bot))
