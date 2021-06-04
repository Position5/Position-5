import logging
from discord.ext import commands
from . import log_to_specific_channel

log = logging.getLogger("position5.error_handler")


class ErrorHandler(commands.Cog):
    "Handles all errors - or just log them :)"

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
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
            log_message = f"Command Not Found | Message: {ctx.message.content} | Author: {ctx.author.name}"
            log.info(log_message)
            await log_to_specific_channel(self.bot, log_message)

        elif isinstance(error, commands.BadArgument):
            log_message = f"Bad arguments to command | Message: {ctx.message.content} | Author: {ctx.author.name}"
            log.error(log_message)
            await log_to_specific_channel(self.bot, log_message, logging.ERROR)
        elif isinstance(error, commands.MissingRequiredArgument):
            log_message = f"Arguments missing: {ctx.command} | Error: {error}"
            log.error(log_message)
            await log_to_specific_channel(self.bot, log_message, logging.ERROR)

        # elif isinstance(error, commands.NoPrivateMessage):
        #     try:
        #         await ctx.author.send(f"{ctx.command} can not be used in Private Messages.")
        #     except discord.HTTPException:
        #         pass

        else:
            log_message = f"Exception in command {ctx.command}"
            log.info(log_message)
            await log_to_specific_channel(self.bot, log_message)
            log.error("Type %s | Error: %s", type(error), error)
            raise error


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
