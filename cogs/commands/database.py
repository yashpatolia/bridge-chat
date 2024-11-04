import discord
from discord.ext import commands
from discord import app_commands
from config import OWNER_ID
from utils.sql_eval import sql_eval


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="db", description="Execute a database command")
    @app_commands.describe(command="Database command to execute")
    async def db(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()
        if interaction.user.id != OWNER_ID:
            return

        results = sql_eval(command)
        embed = discord.Embed(
            colour=discord.Colour.green(),
            description=f"**Command Executed:**\n{results}")
        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Database(client))
