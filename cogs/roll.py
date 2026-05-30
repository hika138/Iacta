import discord
from discord import app_commands
from discord.ext import commands

import modules.myast as myast


class RollCog(commands.Cog):
    def __init__(self, bot: commands.Bot, server_id: int):
        self.bot = bot
        self.guild = discord.Object(id=server_id)

    async def cog_load(self):
        self.bot.tree.add_command(self.roll, guild=self.guild)

    async def cog_unload(self):
        self.bot.tree.remove_command(self.roll.name, type=self.roll.type, guild=self.guild)

    @app_commands.command(name="roll", description="Throw Dice Command")
    @app_commands.rename(formula="式")
    async def roll(self, interaction: discord.Interaction, formula: str):
        tokenizer = myast.Tokenizer(formula)
        try:
            tokens = tokenizer.tokenize()
        except RuntimeError as e:
            await interaction.response.send_message(f"{str(e)}")
            return

        try:
            parser = myast.Parser(tokens)
            ast_tree = parser.parse()
        except ValueError as e:
            await interaction.response.send_message(f"{str(e)}")
            return

        try:
            result = ast_tree.eval()
        except Exception as e:
            await interaction.response.send_message(f"{str(e)}")
            return

        msg = f"{str(interaction.user.display_name)}::`{formula}` > `{str(ast_tree)}` > `{str(result)}`"
        await interaction.response.send_message(msg)


async def setup(bot: commands.Bot):
    server_id = getattr(bot, "server_id", None)
    if server_id is None:
        raise RuntimeError("server_id is not set on bot instance")

    await bot.add_cog(RollCog(bot, int(server_id)))
