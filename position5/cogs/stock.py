import json
from discord.ext import commands
from aiohttp import ClientSession
import discord
import requests
from . import (
    DISCLAIMER,
    NSE_FII_DII,
    NSE_FII_DII_TRADE_REACT,
    WHY_NIFTY,
    delete_message,
    log_params,
)


def gen_embed_fii(json_data):
    embed = discord.Embed(title=f"FII/DII Data: {json_data[0]['date']}")
    for item in json_data:
        embed.add_field(name="\u200b", value="\u200b", inline=False)
        embed.add_field(name=item["category"].split(" ", 1)[0], value="\u200b", inline=False)
        embed.add_field(name="Buy Value", value=item["buyValue"], inline=True).add_field(
            name="Sell Value", value=item["sellValue"], inline=True
        ).add_field(name="Net Value", value=item["netValue"], inline=True)
    return embed


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.__request_headers = {
            "Host": "www.nseindia.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Upgrade-Insecure-Requests": "1",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }
        self.session = requests.Session()
        request = self.session.get(
            NSE_FII_DII,
            headers=self.__request_headers,
            timeout=5,
        )
        self.cookies = dict(request.cookies)

    @commands.command(name="fii", description="latest fii data")
    @delete_message()
    @log_params()
    async def fii(self, ctx):
        async with ClientSession() as session:
            async with session.get(
                NSE_FII_DII_TRADE_REACT,
                headers=self.__request_headers,
            ) as response:
                json_data = json.loads(await response.text())
                if json_data[0]["date"] != json_data[1]["date"]:
                    return
                await ctx.send(embed=gen_embed_fii(json_data))

    @commands.command(name="fiir", description="latest fii data via requests(synchronous)")
    @delete_message()
    @log_params()
    async def fii_synchronous(self, ctx):
        response = self.session.get(
            NSE_FII_DII_TRADE_REACT,
            headers=self.__request_headers,
            timeout=5,
            cookies=self.cookies,
        )
        json_data = response.json()
        if json_data[0]["date"] != json_data[1]["date"]:
            return
        await ctx.send(embed=gen_embed_fii(json_data))

    @commands.command(
        name="disclaimer",
        description="disclaimer",
    )
    @delete_message()
    @log_params()
    async def disclaimer(self, ctx):
        await ctx.send(content=DISCLAIMER)

    @commands.command(name="nifty", description="Why NIFTY")
    @delete_message()
    @log_params()
    async def nifty(self, ctx):
        await ctx.send(
            embed=discord.Embed(
                title="Why trading in NIFTY makes sense?",
                description=WHY_NIFTY,
                color=discord.Color.gold(),
            )
        )


def setup(bot):
    bot.add_cog(Stock(bot))
