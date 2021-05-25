from discord.ext import commands
import discord
from . import log_params


class Embed(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name='embed',
        description='The embed command',
    )
    @log_params()
    async def embed(self, ctx):
        def check(msg):
            return (
                msg.channel == ctx.message.channel and msg.author == ctx.message.author
            )

        await ctx.send(content='What would you like the title to be?')

        msg = await self.bot.wait_for('message', check=check)
        title = msg.content

        await ctx.send(content='What would you like the Description to be?')
        msg = await self.bot.wait_for('message', check=check)
        desc = msg.content

        msg = await ctx.send(content='Now generating the embed...')

        embed = (
            discord.Embed(title=title, description=desc, color=discord.Color.random())
            .set_thumbnail(url=self.bot.user.avatar_url)
            .set_author(
                name=ctx.message.author.name, icon_url=ctx.message.author.avatar_url
            )
        )
        await msg.edit(embed=embed, content=None)

    @commands.command(
        name='help',
        description='The help command!',
        aliases=['commands', 'command'],
        usage='cog',
    )
    @log_params()
    async def help(self, ctx, cog='all'):
        help_embed = discord.Embed(title='Help', color=discord.Color.random())
        help_embed.set_thumbnail(url=self.bot.user.avatar_url)
        help_embed.set_footer(
            text=f'Requested by {ctx.message.author.name}',
            icon_url=ctx.message.author.avatar_url,
        )

        cogs = list(self.bot.cogs.keys())

        if cog == 'all':
            for cog_t in cogs:
                cog_commands = self.bot.get_cog(cog_t).get_commands()
                commands_list = ''
                for comm in cog_commands:
                    commands_list += f'**{comm.name}** - *{comm.description}*\n'
                help_embed.add_field(name=cog_t, value=commands_list, inline=False)
        else:

            lower_cogs = [c.lower() for c in cogs]

            if cog.lower() in lower_cogs:

                commands_list = self.bot.get_cog(
                    cogs[lower_cogs.index(cog.lower())]
                ).get_commands()
                help_text = ''

                for command in commands_list:
                    help_text += (
                        f'```{command.name}```\n' f'**{command.description}**\n\n'
                    )

                    if len(command.aliases) > 0:
                        help_text += (
                            f'**Aliases :** `{"`, `".join(command.aliases)}`\n\n\n'
                        )
                    else:
                        help_text += '\n'

                    help_text += (
                        f'Format: `@{self.bot.user.name}#{self.bot.user.discriminator}'
                        f' {command.name} {command.usage if command.usage is not None else ""}`\n\n\n\n'
                    )
                help_embed.description = help_text
            else:
                await ctx.send(
                    'Invalid cog specified.\nUse `help` command to list all cogs.'
                )
                return

        await ctx.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Embed(bot))
