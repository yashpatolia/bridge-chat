import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_MASTER
from utils.sql_eval import sql_eval

class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="database", description="Execute a database command")
    @app_commands.describe(command="Database command to execute")
    @app_commands.describe(command="How many results to fetch")
    @app_commands.checks.has_role(GUILD_MASTER)
    @app_commands.choices(fetch=[
        app_commands.Choice(name="all", value = 1),
        app_commands.Choice(name="one", value = 2)
    ])
    async def db(self, interaction: discord.Interaction, command: str, fetch: app_commands.Choice[int]) -> None:
        results = sql_eval(command, fetch_all = True if fetch == 1 else False)
        embed = discord.Embed(
            colour=discord.Colour.green(),
            description=f"**Command Executed:**\n{results}")
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Database(client))
