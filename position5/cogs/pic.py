from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
import discord
from discord.ext import commands
from . import delete_message, log_params, EMOTES_PATH, FONT_PATH, MEME_PATH, PIC_PATH, TEMP_PATH


def _get_line_count(draw, text, total_width, font):
    text_width, _ = draw.textsize(text, font)
    if text_width > total_width:
        return int(round((text_width / total_width) + 1))
    return 1


def _get_lines(draw, line_count, text, total_width, font):
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


def draw_text_with_outline(draw, text, text_x, text_y, font):
    draw.text((text_x - 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x - 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y - 2), text, (0, 0, 0), font=font)
    draw.text((text_x + 2, text_y + 2), text, (0, 0, 0), font=font)
    draw.text((text_x, text_y), text, (255, 255, 255), font=font)


def draw_text_with_wrapping(draw, text, total_width, font, offset=(0, 0)):
    left_offset, top_offset = offset
    line_count = _get_line_count(draw, text, total_width, font=font)
    lines = _get_lines(draw, line_count, text, total_width, font=font)

    for i in range(0, line_count):
        width, height = draw.textsize(lines[i], font)
        draw_text_with_outline(draw, lines[i], left_offset + (total_width - width) / 2, top_offset + i * height, font)


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
    async def drake(self, ctx, *, text: str = None):
        if not text:
            await ctx.send(file=discord.File(f"{TEMP_PATH}drake.jpg"))
            return
        if "|" not in text:
            await ctx.send("| is missing")
            return
        first_text, second_text = text.split("|", 1)
        total_width, _ = 450, 360
        first_y, second_y = 50, 510
        left_offset = 550

        template = Image.open(f"{MEME_PATH}drake.jpg")
        draw = ImageDraw.Draw(template)
        font = ImageFont.truetype(f"{FONT_PATH}impact.ttf", 52)

        draw_text_with_wrapping(draw, first_text, total_width, font, (left_offset, first_y))
        draw_text_with_wrapping(draw, second_text, total_width, font, (left_offset, second_y))

        template.save(f"{TEMP_PATH}drake.jpg")
        await ctx.send(file=discord.File(f"{TEMP_PATH}drake.jpg"))


def setup(bot):
    bot.add_cog(Pic(bot))
