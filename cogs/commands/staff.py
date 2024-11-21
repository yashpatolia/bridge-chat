import discord
import sqlite3
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE
from utils.get_uuid import get_uuid

class StaffCommands(commands.GroupCog, name="staff"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="link", description="Link a discord user to a minecraft account!")
    @app_commands.describe(member="Discord User")
    @app_commands.describe(ign="Minecraft Username")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def stafflink(self, interaction: discord.Interaction, member: discord.Member, ign: str) -> None:
        await interaction.response.defer()
        uuid = get_uuid(ign)

        try:
            with sqlite3.connect("temporals.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("SELECT discord_id FROM users WHERE uuid = ?", (uuid,))
                user_check = cursor.fetchone()[0]

                if user_check is not None:
                    cursor.execute("UPDATE users SET discord_id = ?, discord_name = ? WHERE uuid = ?",
                                   (member.id, member.name))
                else:
                    cursor.execute("INSERT INTO users (uuid, ign, discord_id, discord_name) values (?, ?, ?, ?)",
                                   (uuid, ign.lower(), member.id, member.name))

                connection.commit()

            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                description=f"__**Successfully Linked!**__\n"
                            f"**Discord:** {member.name}\n"
                            f"**IGN:** {ign}\n"
                            f"**UUID:** {uuid}")
        except Exception as e:
            embed = discord.Embed(colour=discord.Colour.red(), description=e)

        await interaction.edit_original_response(embed=embed)

async def setup(client):
    await client.add_cog(StaffCommands(client))