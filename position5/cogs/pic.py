from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import discord
from discord.ext import commands
from . import delete_message, log_params, EMOTES_PATH, FONT_PATH, MEME_PATH, PIC_PATH, TEMP_PATH


def draw_text_with_outline(draw, text, text_x, text_y, font):
    draw.text((text_x - 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x - 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x, text_y), text, (255, 255, 255), font=font)


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
    async def kappa(self, ctx, member: discord.Member):
        template = Image.open(f"{EMOTES_PATH}Kappa.png")
        member = member.avatar_url_as(size=64)
        author = ctx.author.avatar_url_as(size=64)
        template.paste(Image.open(BytesIO(await member.read())), (659, 735))
        template.paste(Image.open(BytesIO(await author.read())), (1005, 732))
        template.save(f"{TEMP_PATH}completed.png")
        await ctx.send(file=discord.File(f"{TEMP_PATH}completed.png"))

    @commands.command(name="drake", description="drake meme", usage="text1 | text2")
    @delete_message()
    @log_params()
    async def drake(self, ctx, *, text: str):
        if "|" not in text:
            await ctx.send("| is missing")
            return
        first_text, second_text = text.split("|", 1)

        template = Image.open(f"{MEME_PATH}drake.jpg")
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(f"{FONT_PATH}impact.ttf", 52)

        total_height, total_width = 360, 450
        left_offset = 550

        first_y, second_y = 50, 510

        first_width, first_height = draw.textsize(first_text, font)
        second_width, second_height = draw.textsize(second_text, font)

        draw_text_with_outline(draw, first_text, left_offset + (total_width - first_width) / 2, first_y, font)
        draw_text_with_outline(draw, second_text, left_offset + (total_width - second_width) / 2, second_y, font)

        template.save(f"{TEMP_PATH}drake.jpg")
        await ctx.send(file=discord.File(f"{TEMP_PATH}drake.jpg"))


def setup(bot):
    bot.add_cog(Pic(bot))
