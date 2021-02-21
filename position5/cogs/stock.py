import json
from discord.ext import commands
from aiohttp import ClientSession
import discord


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

    @commands.command(
        name='fii',
        description='latest fii data'
    )
    async def meme(self, ctx):
        await ctx.message.delete()
        async with ClientSession() as session:
            async with session.get('https://www.nseindia.com/api/fiidiiTradeReact', headers=self.__request_headers) as resp:
                json_data = json.loads(await resp.text())
                if json_data[0]['date'] != json_data[1]['date']:
                    return
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
                await ctx.send(embed=embed)
        return


def setup(bot):
    bot.add_cog(Stock(bot))
