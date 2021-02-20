import os
from discord.ext import commands
import discord
from cricapi import Cricapi


class Cricket(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.cricket = Cricapi(os.environ.get('CRIC_API'))

    @commands.command(
        name='cricket',
        description='cricket commands'
    )
    async def cricket_command(self, ctx):
        def check(msg):
            return msg.channel == ctx.message.channel and msg.author == ctx.message.author

        history = {}
        desc = ''
        matches = self.cricket.matches()['matches']
        live_matches = [match for match in matches if match['matchStarted']]
        for count, match in enumerate(live_matches, 1):
            desc += f"\n{count}. {match['team-1']} vs {match['team-2']}"
            history[str(count)] = match['unique_id']
        desc += '\nReply with `<num>` for details'
        await ctx.send(embed=discord.Embed(title='Live cricket matches', description=desc))

        msg = await self.bot.wait_for('message', check=check)
        reply = msg.content.strip()

        if reply in history:
            scores = self.cricket.cricketScore({'unique_id': history[reply]})
            response = discord.Embed(title=scores['score'])
            await ctx.send(embed=response)
        return


def setup(bot):
    bot.add_cog(Cricket(bot))
