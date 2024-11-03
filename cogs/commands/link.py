import discord
import requests
import json
import logging
from discord.ext import commands
from discord import app_commands


class Link(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="link", description="Link minecraft and discord")
    @app_commands.describe(ign="Enter an IGN")
    async def link(self, interaction: discord.Interaction, ign: str):
        await interaction.response.defer()
        try:
            data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{ign}").json()
            logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{ign}")
            profile = list(data['profiles'].keys())[0]
            discord_name = data['profiles'][profile]['data']['social']['DISCORD']
            username = data['profiles'][profile]['data']['display_name']
            uuid = data['profiles'][profile]['data']['uuid']

            with open('discord.json', 'r') as file:
                discord_data = json.load(file)

            discord_data['users'][interaction.user.id] = uuid

            with open('discord.json', 'w') as file:
                file.write(json.dumps(discord_data, indent=4))

            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"__**Successfully Linked!**__\n"
                            f"**Discord:** {discord_name}\n"
                            f"**IGN:** {username}")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            logging.error(e)
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description=f"Error looking up IGN")
            await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Link(client))
