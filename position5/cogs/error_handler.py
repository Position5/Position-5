import logging
from discord.ext import commands

log = logging.getLogger("position5.error_handler")


class ErrorHandler(commands.Cog):
    "Handles all errors - or just log them :)"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers being handled here in on_command_error.
        if hasattr(ctx.command, "on_error"):
            return

        # Allows us to check for original exceptions raised and sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to on_command_error.
        error = getattr(error, "original", error)

        if isinstance(error, commands.CommandNotFound):
            log.info(
                "Command Not Found | Message: %s | Author: %s",
                ctx.message.content,
                ctx.author.name,
            )

        elif isinstance(error, commands.BadArgument):
            await ctx.send("Bad arguments to command")

        # elif isinstance(error, commands.DisabledCommand):
        #     await ctx.send(f"{ctx.command} has been disabled.")

        # elif isinstance(error, commands.NoPrivateMessage):
        #     try:
        #         await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
        #     except discord.HTTPException:
        #         pass

        else:
            log.info("Exception in command %s", ctx.command)
            log.error("Type %s | Error: %s", type(error), error)
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
