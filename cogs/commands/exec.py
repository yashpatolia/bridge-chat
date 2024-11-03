import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE


class Exec(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="exec", description="Execute a command")
    @app_commands.describe(command="Command to run in game (don't add /)")
    async def exec(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()

        staff_role = interaction.guild.get_role(STAFF_ROLE)
        if staff_role not in interaction.user.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="Not sufficient permissions!")
        else:
            self.client.bot.chat(f"/{command}")
            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"**Command Executed:** /{command}")

        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Exec(client))
