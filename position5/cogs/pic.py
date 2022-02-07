from io import BytesIO
from PIL import Image
import discord
from discord.ext import commands
from glitch_this import ImageGlitcher
from . import delete_message, log_params, EMOTES_PATH, PIC_PATH, TEMP_PATH


class Pic(commands.Cog):
    "Image processing"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.glitcher = ImageGlitcher()

    @commands.command(name="xdoubt", description="xdoubt pic")
    @delete_message()
    @log_params()
    async def xdoubt(self, ctx: commands.Context):
        await ctx.send(file=discord.File(f"{PIC_PATH}xdoubt.png"))

    @commands.command(name="kappa", description="make kappa eyes")
    @delete_message()
    @log_params()
    async def kappa(self, ctx: commands.Context, member: discord.Member):
        template = Image.open(f"{EMOTES_PATH}Kappa.png")
        member = member.avatar_url_as(size=64)
        author = ctx.author.avatar_url_as(size=64)
        template.paste(Image.open(BytesIO(await member.read())), (659, 735))
        template.paste(Image.open(BytesIO(await author.read())), (1005, 732))
        template.save(f"{TEMP_PATH}completed.png")
        await ctx.send(file=discord.File(f"{TEMP_PATH}completed.png"))

    @commands.command(
        name="glitch",
        description="glitch image color",
        usage="upload image(float 0-10)",
    )
    @delete_message()
    @log_params()
    async def glitch_color(self, ctx: commands.Context, amount: float = 2.718):
        for att in ctx.message.attachments:
            image = Image.open(BytesIO(await att.read()))
            glitch_img = self.glitcher.glitch_image(image, amount, color_offset=True)
            glitch_img.save(f"{TEMP_PATH}glitch.png")
            await ctx.send(file=discord.File(f"{TEMP_PATH}glitch.png"))

    @commands.command(
        name="glitchp",
        description="glitch image position",
        usage="upload image(float 0-10)",
    )
    @delete_message()
    @log_params()
    async def glitch_position(self, ctx: commands.Context, amount: float = 2.718):
        for att in ctx.message.attachments:
            image = Image.open(BytesIO(await att.read()))
            glitch_img = self.glitcher.glitch_image(image, amount, color_offset=False)
            glitch_img.save(f"{TEMP_PATH}glitch.png")
            await ctx.send(file=discord.File(f"{TEMP_PATH}glitch.png"))


def setup(bot):
    bot.add_cog(Pic(bot))
