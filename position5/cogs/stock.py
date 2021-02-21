import json
from discord.ext import commands
from aiohttp import ClientSession
import discord
import requests


def gen_embed_fii(json_data):
    embed = discord.Embed(title=f"FII/DII Data: {json_data[0]['date']}")
    for item in json_data:
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name=item['category'].split(' ', 1)[0], value='\u200b', inline=False)
        embed.add_field(
            name='Buy Value', value=item['buyValue'], inline=True
        ).add_field(
            name='Sell Value', value=item['sellValue'], inline=True
        ).add_field(
            name='Net Value', value=item['netValue'], inline=True
        )
    return embed


class Stock(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.__request_headers = {
            'Host': 'www.nseindia.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101 Firefox/82.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
        self.session = requests.Session()
        request = self.session.get('https://www.nseindia.com/reports/fii-dii', headers=self.__request_headers, timeout=5)
        self.cookies = dict(request.cookies)

    @commands.command(
        name='fii',
        description='latest fii data'
    )
    async def fii_command(self, ctx):
        await ctx.message.delete()
        async with ClientSession() as session:
            async with session.get('https://www.nseindia.com/api/fiidiiTradeReact', headers=self.__request_headers) as resp:
                json_data = json.loads(await resp.text())
                if json_data[0]['date'] != json_data[1]['date']:
                    return
                await ctx.send(embed=gen_embed_fii(json_data))
        return

    @commands.command(
        name='fiir',
        description='latest fii data via requests(synchronous)'
    )
    async def fii_synchronous_command(self, ctx):
        await ctx.message.delete()
        response = self.session.get('https://www.nseindia.com/api/fiidiiTradeReact', headers=self.__request_headers, timeout=5, cookies=self.cookies)
        json_data = response.json()
        if json_data[0]['date'] != json_data[1]['date']:
            return
        await ctx.send(embed=gen_embed_fii(json_data))
        return


def setup(bot):
    bot.add_cog(Stock(bot))
