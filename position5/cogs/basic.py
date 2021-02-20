from datetime import datetime as dt
import random
from discord.ext import commands, tasks
import discord


class Basic(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.support_activities = [
            discord.Game(name="Dota 2"), discord.Streaming(name="Dota 2", url="https://www.twitch.tv/dreamleague"),
            discord.Activity(type=discord.ActivityType.listening, name="Gucci gang"),
            discord.Activity(type=discord.ActivityType.watching, name="DOTA: Dragon's Blood"),
            discord.Game(name="Dota 2"), discord.Streaming(name="Dota 2", url="https://www.twitch.tv/MiaMalkova"),
            discord.Activity(type=discord.ActivityType.watching, name="Snyder Cut"),
        ]
        self.change_activity.start()

    @commands.command(
        name='ping',
        description='The ping command',
        aliases=['p']
    )
    async def ping_command(self, ctx):
        start = dt.timestamp(dt.now())
        # Gets the timestamp when the command was used

        msg = await ctx.send(content='Pinging')
        # Sends a message to the user in the channel the message with the command was received.
        # Notifies the user that pinging has started

        await msg.edit(content=f'Pong!\nOne message round-trip took {(dt.timestamp(dt.now())-start) * 1000}ms.')
        # Ping completed and round-trip duration show in ms
        # Since it takes a while to send the messages, it will calculate how much time it takes to edit an message.
        # It depends usually on your internet connection speed

        return

    @commands.command(
        name='say',
        description='The say command',
        aliases=['repeat', 'parrot'],
        usage='<text>'
    )
    async def say_command(self, ctx):
        # The 'usage' only needs to show the parameters
        # As the rest of the format is generated automatically

        # Lets see what the parameters are: -
        # The self is just a regular reference to the class
        # ctx - is the Context related to the command
        # For more reference - https://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html#context

        # Next we get the message with the command in it.
        msg = ctx.message.content

        await ctx.message.delete()

        # Extracting the text sent by the user
        # ctx.invoked_with gives the alias used
        # ctx.prefix gives the prefix used while invoking the command
        prefix_used = ctx.prefix
        alias_used = ctx.invoked_with
        text = msg[len(prefix_used) + len(alias_used):].strip()

        # Next, we check if the user actually passed some text
        if text == '':
            # User didn't specify the text
            await ctx.send(content='You need to specify the text!')

        else:
            # User specified the text.
            await ctx.send(content=text)

        return

    @tasks.loop(seconds=10.0)
    async def change_activity(self):
        await self.bot.change_presence(activity=random.choice(self.support_activities))

    @change_activity.before_loop
    async def before_change_activity(self):
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Basic(bot))
    # Adds the Basic commands to the bot
    # Note: The "setup" function has to be there in every cog file
