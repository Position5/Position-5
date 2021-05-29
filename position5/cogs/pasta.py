import discord
from discord.ext import commands
from . import delete_message, log_params, parse_xml


class Pasta(commands.Cog):
    "Your next door copypasta"

    def __init__(self, bot):
        self.bot = bot
        self.pastas = {}
        self._refresh_pasta()

    def _refresh_pasta(self):
        root = parse_xml("assets/pasta.xml")
        self.pastas.clear()
        for pasta in root:
            if pasta.tag == "fixed":
                self.pastas[pasta.attrib["name"]] = pasta.text

    @commands.command(name="refp", description="refresh pasta")
    @delete_message()
    @log_params()
    async def refresh_pasta(self, ctx):
        self._refresh_pasta()

    @commands.command(name="pastas", description="sends list of pasta", usage="<search_string>", aliases=["lp"])
    @delete_message()
    @log_params()
    async def list_pasta(self, ctx):
        pastas = self.pastas.keys()
        title = "Available pastas:"
        description = ""
        desc_list = []

        for pasta in pastas:
            description += f"\n➥ {pasta}"
            if len(description) >= 1900:
                desc_list.append(description)
                description = ""

        if description != "":
            desc_list.append(description)

        total_count = len(desc_list)

        for count, desc in enumerate(desc_list, 1):
            await ctx.send(
                embed=discord.Embed(
                    title=f"{title} [{count}/{total_count}]",
                    description=desc,
                    color=discord.Color.random(),
                )
            )

    @commands.command(name="pasta", description="copy pasta")
    @delete_message()
    @log_params()
    async def pasta_without_variables(self, ctx, *, pasta_name: str):
        print(repr(pasta_name))
        if pasta_name.lower() in self.pastas:
            await ctx.send(self.pastas[pasta_name.lower()])


def setup(bot):
    bot.add_cog(Pasta(bot))
