import discord
import requests
import logging
import sqlite3
from discord.ext import commands
from discord import app_commands
from utils.get_uuid import get_uuid

class Link(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="link", description="Link minecraft and discord")
    @app_commands.describe(ign="Enter an IGN")
    async def link(self, interaction: discord.Interaction, ign: str) -> None:
        await interaction.response.defer()

        try:
            data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{ign}").json()
            logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{ign}")
            profile = list(data['profiles'].keys())[0]
            discord_name = data['profiles'][profile]['data']['social']['DISCORD']
            username = data['profiles'][profile]['data']['display_name']
            uuid = get_uuid(ign)

            if discord_name != interaction.user.name:
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    description=f"Your discord in-game is not linked correctly.")
                await interaction.edit_original_response(embed=embed)
                return

            with sqlite3.connect("temporals.db") as connection:
                cursor = connection.cursor()
                connection.execute("PRAGMA foreign_keys = ON;")

                cursor.execute("SELECT discord_id FROM users WHERE uuid = ?", (uuid,))
                user_check = cursor.fetchone()[0]

                if user_check is not None:
                    embed = discord.Embed(
                        colour=discord.Colour.green(),
                        description=f"Already Linked.")
                    await interaction.edit_original_response(embed=embed)
                    return

                cursor.execute("UPDATE users SET discord_id = ?, discord_name = ? WHERE uuid = ?",
                        (interaction.user.id, discord_name, uuid))
                connection.commit()

            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"__**Successfully Linked!**__\n"
                            f"**Discord:** {discord_name}\n"
                            f"**IGN:** {username}\n"
                            f"**UUID:** {uuid}")
            await interaction.edit_original_response(embed=embed)

        except Exception as e:
            logging.error(e)
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                description=f"Error looking up IGN")
            await interaction.edit_original_response(embed=embed)

async def setup(client):
    await client.add_cog(Link(client))
