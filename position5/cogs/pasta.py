from string import Template
import discord
from discord.ext import commands
from . import delete_message, log_params, parse_xml


class Pasta(commands.Cog):
    "Your next door copypasta"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.fixed = {}
        self.variable = {}
        self._refresh_pasta()

    def _refresh_pasta(self):
        root = parse_xml("assets/pasta.xml")
        self.fixed.clear()
        self.variable.clear()
        for pasta in root:
            if pasta.tag == "fixed":
                self.fixed[pasta.attrib["name"]] = pasta.text
            elif pasta.tag == "variable":
                self.variable[pasta.attrib["name"]] = (pasta.text, pasta.attrib["vars"])

    @commands.command(name="refp", description="refresh pasta")
    @delete_message()
    @log_params()
    async def refresh_pasta(self, ctx: commands.Context):
        self._refresh_pasta()

    @commands.command(
        name="pastas",
        description="sends list of pasta",
        usage="<search_string>",
        aliases=["lp"],
    )
    @delete_message()
    @log_params()
    async def list_pasta(self, ctx: commands.Context):
        pastas = list(self.fixed.keys()) + list(self.variable.keys())
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
    async def pasta_without_variables(
        self, ctx: commands.Context, pasta_name: str, *, var: str = ""
    ):
        if pasta_name.lower() in self.fixed:
            await ctx.send(self.fixed[pasta_name.lower()])
        elif pasta_name.lower() in self.variable:
            pasta = self.variable[pasta_name.lower()]
            _vars = var.split("|")
            _t_vars = pasta[1].split(",")
            if len(_vars) != len(_t_vars):
                return
            template = Template(pasta[0])
            gen_text = template.substitute(dict(zip(_t_vars, _vars)))
            await ctx.send(gen_text)


def setup(bot):
    bot.add_cog(Pasta(bot))
