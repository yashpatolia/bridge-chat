import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE

class Exec(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="exec", description="Execute a command")
    @app_commands.describe(command="Command to run in game (don't add /)")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def exec(self, interaction: discord.Interaction, command: str) -> None:
        self.client.bot.chat(f"/{command}")
        embed = discord.Embed(colour=discord.Colour.green(), description=f"**Command Executed:** /{command}")
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Exec(client))
