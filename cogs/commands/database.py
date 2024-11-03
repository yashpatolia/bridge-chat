import discord
import sqlite3
import logging
from discord.ext import commands
from discord import app_commands
from config import OWNER_ID


class Database(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="db", description="Execute a database command")
    @app_commands.describe(command="Database command to execute")
    async def db(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()
        if interaction.user.id != OWNER_ID:
            return

        connection = sqlite3.connect('temporals.db')
        cursor = connection.cursor()
        try:
            cursor.execute(f'''{command}''')
            results = cursor.fetchall()
            connection.commit()
            connection.close()
            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"**Command Executed:**\n"
                            f"{results}")
        except Exception as e:
            logging.error(e)
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description=f"**Error Executing:**\n"
                            f"{e}")

        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Database(client))
