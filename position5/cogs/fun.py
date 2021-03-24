from discord.ext import commands
import aiohttp
import discord
from . import AGIFY, GENDERIFY


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command(
        name='who',
        description='fun game which predicts your age, gender, country(ISO 3166-1 alpha-2)',
        usage='<name> <country-optional>',
        alisaes=['whoami'],
    )
    async def whoami(self, ctx, name: str = None, *, country: str = None):
        await ctx.message.delete()
        params = {}
        if name:
            params['name'] = name
        else:
            params['name'] = ctx.message.author.name
        if country:
            params['country_id'] = country

        age_resp = await self.session.get(AGIFY, params=params)
        gender_resp = await self.session.get(GENDERIFY, params=params)
        age = await age_resp.json()
        gender = await gender_resp.json()

        embed = discord.Embed(
            title='Here\'s a guess',
            description=f'Name: {params.get("name") or ""}\nAge: {age.get("age") or ""}\nGender: {gender.get("gender").title() or ""}({gender.get("probability") * 100 or 0}%)',
            color=discord.Color.random(),
        )

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
