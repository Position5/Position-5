import asyncio
import discord
from discord.ext import commands


class Poll(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='poll',
        description='poll without custom options'
    )
    async def poll_without_options(self, ctx, *, question):
        await ctx.message.delete()
        reactions = ['✅', '❌', '💤']
        embed = discord.Embed(
            title=question
        ).set_footer(
            text='Poll will end in 100 seconds! Please react once.'
        ).set_author(
            name=ctx.message.author.name,
            icon_url=ctx.message.author.avatar_url
        )
        message = await ctx.send(embed=embed)
        for reaction in reactions:
            await message.add_reaction(reaction)

        await asyncio.sleep(10)

        total_count = -3
        reaction_count = {}

        message_after = await ctx.fetch_message(message.id)
        for reaction in message_after.reactions:
            total_count += reaction.count
            reaction_count[reaction.emoji] = reaction.count

        yes_count = reaction_count.get('✅', 1) - 1
        no_count = reaction_count.get('❌', 1) - 1

        results = discord.Embed(
            title='Results',
            description=f'Asked: **{question}**\n\n✅ : Yes({yes_count})\n\n❌ : No({no_count}) \n\n💤 : Don\'t care({total_count - yes_count - no_count})'
        )
        await ctx.send(embed=results)


def setup(bot):
    bot.add_cog(Poll(bot))
