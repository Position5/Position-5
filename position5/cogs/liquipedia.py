from datetime import timedelta
import requests
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from dateutil import parser
from . import delete_message, log_params, LIQUIPEDIA_ICON


class Liquipedia(commands.Cog):
    """Liquipedia Dota"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="dota", description="dota schedule", aliases=["animajor", "major"])
    @delete_message()
    @log_params()
    async def dota_schedule(self, ctx: commands.Context, *, url: str = ""):
        if not url:
            url = "https://liquipedia.net/dota2/WePlay/AniMajor/2021"
        _resp = requests.get(url)
        soup = BeautifulSoup(_resp.text, "html.parser")

        upcoming_matches = soup.find(string="Upcoming Matches")
        tables = upcoming_matches.find_parent("div").find_parent("div").find_parent("div").find_all("table")

        title = soup.title.text.split("-")[0].strip()
        description = ""

        for table in tables:
            for tbody in table.find_all("tbody"):
                rows = tbody.find_all("tr")
                teams = rows[0].find_all("td")
                stream_info = rows[1].td
                time = parser.parse(stream_info.span.span.text) + timedelta(hours=5, minutes=30)

                description += f"{stream_info.div.div.text}\n"
                description += f"{teams[0].span['data-highlightingclass']}"
                description += f" {teams[1].text} {teams[2].span['data-highlightingclass']}\n"
                description += f"Time: {time.strftime('%b %d, %Y %H:%M')}\n"
                description += f"Watch on: https://twitch.tv/{stream_info.span.span['data-stream-twitch']}\n\n"

        await ctx.send(
            embed=discord.Embed(title=title, description=description)
            .set_author(
                name="Schedule here",
                url=url,
                icon_url=LIQUIPEDIA_ICON,
            )
            .set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar_url)
        )


def setup(bot):
    bot.add_cog(Liquipedia(bot))
