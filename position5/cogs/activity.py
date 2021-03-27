from datetime import timedelta as td
import random
import discord
from discord.ext import commands, tasks


class Activity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.support_activities = [
            discord.Game(name="Dota 2"),
            discord.Streaming(name="Dota 2", url="https://www.twitch.tv/dreamleague"),
            discord.Activity(type=discord.ActivityType.listening, name="Gucci gang"),
            discord.Activity(
                type=discord.ActivityType.watching, name="DOTA: Dragon's Blood"
            ),
            discord.Streaming(name="Dota 2", url="https://www.twitch.tv/MiaMalkova"),
            discord.Activity(type=discord.ActivityType.watching, name="Snyder Cut"),
        ]
        self.change_activity.start()

    @tasks.loop(seconds=10.0)
    async def change_activity(self):
        await self.bot.change_presence(activity=random.choice(self.support_activities))

    @change_activity.before_loop
    async def before_change_activity(self):
        await self.bot.wait_until_ready()

    @commands.command(
        name='activity',
        description='check activities of user',
        usage='<user>',
        aliases=['act', 'spotify'],
    )
    async def activity(self, ctx, user: discord.Member = None):
        await ctx.message.delete()

        if user is None:
            user = ctx.author

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, discord.Spotify):
                    embed = (
                        discord.Embed(
                            title=f"{user.name}'s Spotify",
                            description="Listening to {}".format(activity.title),
                            color=activity.color,
                        )
                        .set_thumbnail(url=activity.album_cover_url)
                        .add_field(name="Artist", value=activity.artist)
                        .add_field(name="Album", value=activity.album)
                    )
                    if activity.created_at:
                        embed.set_footer(
                            text=f"Song started at {(activity.created_at + td(hours=5, minutes=30)).strftime('%H:%M:%S')}"
                        )
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.Game):
                    embed = discord.Embed(
                        title=f"{user.name}'s Game",
                        description="Playing {}".format(activity.name),
                        color=discord.Color.random(),
                    )
                    if activity.start:
                        embed.set_footer(
                            text=f"Game started at {(activity.start + td(hours=5, minutes=30)).strftime('%H:%M:%S')}"
                        )
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.Streaming):
                    embed = discord.Embed(
                        title=f"{user.name}'s Stream",
                        description=f"Streaming {activity.name}",
                        color=discord.Color.random(),
                    )
                    embed.set_footer(text=f"Streaming at {activity.url}")
                    await ctx.send(embed=embed)
                elif isinstance(activity, discord.activity.CustomActivity):
                    await ctx.send(
                        content=f'Status: {activity.emoji or ""} {activity.name}'
                    )
                else:
                    await ctx.send(
                        content=f'{activity.type.name.title()} {activity.name}'
                    )


def setup(bot):
    bot.add_cog(Activity(bot))
