from io import BytesIO
from PIL import Image
import discord
from discord.ext import commands
from . import delete_message, log_params, PIC_PATH


class Pic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="xdoubt", description="xdoubt pic")
    @delete_message()
    @log_params()
    async def xdoubt(self, ctx):
        await ctx.send(file=discord.File(f"{PIC_PATH}xdoubt.png"))

    @commands.command(name="kappa", description="make kappa eyes")
    @delete_message()
    @log_params()
    async def push(self, ctx, member: discord.Member):
        im1 = Image.open("assets/emotes/Kappa.png")
        asset2 = member.avatar_url_as(size=64)
        asset3 = ctx.author.avatar_url_as(size=64)
        data2 = BytesIO(await asset2.read())
        data3 = BytesIO(await asset3.read())
        im2 = Image.open(data2)
        im3 = Image.open(data3)
        im1.paste(im2, (659, 735))
        im1.paste(im3, (1005, 732))
        im1.save("assets/tmp/completed.png")
        await ctx.send(file=discord.File("assets/tmp/completed.png"))


def setup(bot):
    bot.add_cog(Pic(bot))
