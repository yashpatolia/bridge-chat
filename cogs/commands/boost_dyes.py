import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE, DYE_EMOJIS
from typing import List

class BoostDyes(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="boost-dyes", description=f"Select 3 dyes to boost odds")
    @app_commands.describe(dye1="Dye gets 3x boosted odds")
    @app_commands.describe(dye2="Dye gets 2x boosted odds")
    @app_commands.describe(dye3="Dye gets 2x boosted odds")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def boostdyes(self, interaction: discord.Interaction, dye1: str, dye2: str, dye3: str) -> None:
        await interaction.response.defer()

        with sqlite3.connect("temporals.db") as connection:
            cursor = connection.cursor()
            connection.execute("PRAGMA foreign_keys = ON;")

            cursor.execute("UPDATE dyes SET rate = ?", (1,))
            cursor.execute("UPDATE dyes SET rate = ? WHERE dye_id = ?", (3, dye1))
            cursor.execute("UPDATE dyes SET rate = ? WHERE dye_id = ?", (2, dye2))
            cursor.execute("UPDATE dyes SET rate = ? WHERE dye_id = ?", (2, dye3))
            connection.commit()

        embed = discord.Embed(
            colour=discord.Colour.dark_green(),
            description=f"**Buffed Dye Odds**\n"
                        f"<:{dye1}:{DYE_EMOJIS[dye1]}> **{dye1.replace('_', ' ').lower()}:** 3x More Common\n"
                        f"<:{dye2}:{DYE_EMOJIS[dye2]}> **{dye2.replace('_', ' ').lower()}:** 2x More Common\n"
                        f"<:{dye3}:{DYE_EMOJIS[dye3]}> **{dye3.replace('_', ' ').lower()}:** 2x More Common")
        await interaction.edit_original_response(embed=embed)

    @boostdyes.autocomplete('dye1')
    @boostdyes.autocomplete('dye2')
    @boostdyes.autocomplete('dye3')
    async def dyes_autocomplete(self, interaction: discord.Interaction, current: str) -> List[app_commands.Choice[str]]:
        with sqlite3.connect("temporals.db") as connection:
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
    await client.add_cog(BoostDyes(client))
