import asyncio
import discord
import logging
import sqlite3
from discord.ext import commands
from discord import app_commands
from config import GUILD_MEMBER, PAST, PRESENT, FUTURE
from utils.get_skyblock_level import get_skyblock_level

class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="roles", description="Claim all available roles")
    async def roles(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        try:
            roles = ""
            roles_to_give = []
            guild_member = interaction.guild.get_role(GUILD_MEMBER)

            with sqlite3.connect("temporals.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("SELECT ign FROM users WHERE discord_id = ?", (interaction.user.id,))
                result = cursor.fetchone()

                if result is not None:
                    ign = result[0]
                    if guild_member in interaction.user.roles:  # Guild Roles
                        sb_level = get_skyblock_level(ign)

                        if 250 <= sb_level < 300:
                            roles_to_give.append(interaction.guild.get_role(PAST))
                        elif 300 <= sb_level < 350:
                            roles_to_give.append(interaction.guild.get_role(PRESENT))
                        elif 350 <= sb_level:
                            roles_to_give.append(interaction.guild.get_role(FUTURE))

                else:
                    embed = discord.Embed(
                        colour=discord.Colour.dark_red(),
                        description=f"**Not Linked!**\n"
                                    f"Run `/link (ign)`")
                    await interaction.edit_original_response(embed=embed)

            for role in roles_to_give:
                roles += f"{role.mention} "
                await interaction.user.add_roles(role)
                await asyncio.sleep(0.2)

            embed = discord.Embed(colour=discord.Colour.teal(), description="You already have all the roles!")
            if roles != "":
                embed.description = (
                    "**Successfully Added Roles!**\n"
                    f"**Roles:** {roles}")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            logging.error(e)

async def setup(client):
    await client.add_cog(Roles(client))
