from typing import Tuple
from PIL import Image, ImageFont, ImageDraw
import discord
from discord.ext import commands
from . import delete_message, log_params, FONT_PATH, MEME_PATH, TEMP_PATH


def _get_line_count(draw: ImageDraw, text: str, total_width: int, font: ImageFont):
    text_width, _ = draw.textsize(text, font)
    if text_width > total_width:
        return int(round((text_width / total_width) + 1))
    return 1


def _get_lines(draw: ImageDraw, line_count: int, text: str, total_width: int, font: ImageFont):
    lines = []
    if line_count > 1:
        last_cut = 0
        is_last = False
        for i in range(0, line_count):
            cut = last_cut
            if last_cut == 0:
                cut = int(len(text) / line_count) * i

            if i < line_count - 1:
                next_cut = int(len(text) / line_count) * (i + 1)
            else:
                next_cut = len(text)
                is_last = True

            # make sure we don't cut words in half
            if not (next_cut == len(text) or text[next_cut] == " "):
                while text[next_cut] != " ":
                    next_cut += 1

            line = text[cut:next_cut].strip()

            # is line still fitting ?
            width, _ = draw.textsize(line, font)
            if not is_last and width > total_width:
                next_cut -= 1
                while text[next_cut] != " ":
                    next_cut -= 1

            last_cut = next_cut
            lines.append(text[cut:next_cut].strip())
    else:
        lines.append(text)
    return lines


def draw_text_with_outline(draw: ImageDraw, text: str, text_x: int, text_y: int, font: ImageFont):
    draw.text((text_x - 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x - 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x, text_y), text, (255, 255, 255), font=font)


def draw_text_with_wrapping(
    draw: ImageDraw, text: str, total_width: int, font: ImageFont, offset: Tuple[int, int] = (0, 0)
):
    left_offset, top_offset = offset
    line_count = _get_line_count(draw, text, total_width, font=font)
    lines = _get_lines(draw, line_count, text, total_width, font=font)

    for i in range(0, line_count):
        width, height = draw.textsize(lines[i], font)
        draw_text_with_outline(draw, lines[i], left_offset + (total_width - width) / 2, top_offset + i * height, font)


class Meme(commands.Cog):
    "Meme Templates"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="drake", description="drake meme", usage="text1 | text2")
    @delete_message()
    @log_params()
    async def drake(self, ctx: commands.Context, *, text: str = ""):
        if not text:
            await ctx.send(file=discord.File(f"{TEMP_PATH}drake.jpg"))
            return
        if "|" not in text:
            await ctx.send("| is missing")
            return
        first_text, second_text = map(str.strip, text.split("|", 1))
        total_width, _ = 450, 360
        first_offset = (550, 50)
        second_offset = (550, 510)

        template = Image.open(f"{MEME_PATH}drake.jpg")
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(f"{FONT_PATH}impact.ttf", 52)

        draw_text_with_wrapping(draw, first_text, total_width, font, first_offset)
        draw_text_with_wrapping(draw, second_text, total_width, font, second_offset)

        template.save(f"{TEMP_PATH}drake.jpg")
        await ctx.send(file=discord.File(f"{TEMP_PATH}drake.jpg"))

    @commands.command(name="truth", description="tell me the truth(peter parker) meme", usage="small sentence")
    @delete_message()
    @log_params()
    async def tell_me_the_truth(self, ctx: commands.Context, *, text: str = ""):
        if not text:
            await ctx.send(file=discord.File(f"{TEMP_PATH}truth.jpg"))
            return
        template = Image.open(f"{MEME_PATH}truth.jpg")
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(f"{FONT_PATH}impact.ttf", 22)

        offset = (60, 520)
        total_width = 400
        draw_text_with_wrapping(draw, text, total_width, font, offset)

        template.save(f"{TEMP_PATH}truth.jpg")
        await ctx.send(file=discord.File(f"{TEMP_PATH}truth.jpg"))


def setup(bot):
    bot.add_cog(Meme(bot))
