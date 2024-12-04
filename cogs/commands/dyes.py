import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from config import DYE_ROLES, DYE_EMOJIS
from typing import List

class Dyes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="dyes", description="Show owned dyes & select color")
    @app_commands.describe(dye="Enter a dye to recieve the color role")
    async def dyes(self, interaction: discord.Interaction, dye: str) -> None:
        await interaction.response.defer()
        for dye_id, dye_role_id in DYE_ROLES.items():
            dye_role = interaction.guild.get_role(dye_role_id)
            if dye_role in interaction.user.roles:
                await interaction.user.remove_roles(dye_role)
                break
        selected_dye_role = interaction.guild.get_role(DYE_ROLES[dye])
        await interaction.user.add_roles(selected_dye_role)

        with sqlite3.connect("bridge.db") as connection:
            cursor = connection.cursor()
            connection.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("SELECT hex, dye_name FROM dyes WHERE dye_id = ?", (dye,))
            results = cursor.fetchone()

        embed = discord.Embed(
            color = discord.Color.from_str(f"#{results[0].lower()}"),
            description = f"**Selected:** <:{dye}:{DYE_EMOJIS[dye]}> {results[1]}")

        await interaction.edit_original_response(embed=embed)

    @dyes.autocomplete('dye')
    async def dyes_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        with sqlite3.connect("bridge.db") as connection:
            cursor = connection.cursor()
            connection.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("SELECT uuid FROM users WHERE discord_id = ?", (interaction.user.id,))
            uuid = cursor.fetchone()
            if uuid is None:
                return []
            uuid = uuid[0]

            cursor.execute("SELECT dye_id FROM users_dyes WHERE uuid = ? AND received = TRUE", (uuid,))
            unlocked_dyes = cursor.fetchall()

        return [
            app_commands.Choice(name=dye_id[0].replace('_', ' ').title(), value=dye_id[0])
            for dye_id in unlocked_dyes if current.lower() in dye_id[0].replace('_', ' ').lower()
        ]

async def setup(client):
    await client.add_cog(Dyes(client))
