from datetime import timedelta as td
import discord
from discord.ext import commands


class Activity(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='activity',
        description='check activities of user',
        usage='<user>',
        aliases=['act', 'spotify']

    )
    async def activity(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, discord.Spotify):
                    embed = discord.Embed(
                        title=f"{user.name}'s Spotify",
                        description="Listening to {}".format(activity.title),
                        color=activity.color)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    embed.set_footer(text=f"Song started at {(activity.created_at + td(hours=5, minutes=30)).strftime('%H:%M:%S')}")
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.Game):
                    embed = discord.Embed(
                        title=f"{user.name}'s Game",
                        description="Playing {}".format(activity.name),
                        color=0xC902FF)
                    embed.set_footer(text=f"Game started at {(activity.start + td(hours=5, minutes=30)).strftime('%H:%M:%S')}")
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.Streaming):
                    embed = discord.Embed(
                        title=f"{user.name}'s Stream",
                        description=f"Streaming {activity.name}",
                        color=0xC902FF)
                    embed.set_footer(text=f"Streaming at {activity.url}")
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.CustomActivity):
                    await ctx.send(content=f'Status: {activity.emoji or ""} {activity.name}')
                else:
                    await ctx.send(content=f'{activity.type.name.title()} {activity.name}')


def setup(bot):
    bot.add_cog(Activity(bot))
