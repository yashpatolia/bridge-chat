import asyncio
import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from config import OWNER_ID


class AdminCommands(commands.GroupCog, name="admin"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="add-dye", description="Add a dye to the database!")
    @app_commands.describe(dye_id="Dye ID")
    @app_commands.describe(dye_name="Dye Name")
    @app_commands.describe(weight="Weight in Decimals")
    @app_commands.describe(hex="Hex Color")
    async def adddye(self, interaction: discord.Interaction, dye_id: str, dye_name: str, weight: float, hex: str):
        if interaction.user.id != OWNER_ID:
            return

        await interaction.response.defer()
        try:
            with sqlite3.connect("temporals.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("INSERT INTO dyes (dye_id, dye_name, weight, hex) values (?, ?, ?, ?)",
                               (dye_id, dye_name.title(), weight, hex.capitalize()))
                connection.commit()
        except Exception as e:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description=e)

        embed = discord.Embed(
            colour=discord.Colour.green(),
            description=f"**Successfully Added:** {dye_name}!")
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="remove-dye", description="Remove a dye from the database!")
    @app_commands.describe(dye_id="Dye ID")
    async def removedye(self, interaction: discord.Interaction, dye_id: str):
        if interaction.user.id != OWNER_ID:
            return

        await interaction.response.defer()
        try:
            with sqlite3.connect("temporals.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("DELETE FROM dyes WHERE dye_id = ?", (dye_id,))
                connection.commit()

                embed = discord.Embed(
                    colour=discord.Colour.green(),
                    description=f"**Successfully Removed:** {dye_id}!")
        except Exception as e:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description=e)

        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(AdminCommands(client))