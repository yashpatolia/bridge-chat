import asyncio
import discord
import json
import logging
import requests
from discord.ext import commands
from discord import app_commands
from config import GUILD_MEMBER


class Roles(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="roles", description="Claim all available roles (Requires /verify)")
    async def roles(self, interaction: discord.Interaction):
        await interaction.response.defer()

        try:
            roles = ""
            roles_to_give = []
            guild_member = interaction.guild.get_role(GUILD_MEMBER)

            with open('discord.json', 'r') as file:
                discord_data = json.load(file)

            with open('users.json', 'r') as file:
                user_data = json.load(file)

            if str(interaction.user.id) not in discord_data['users'].keys():  # Not Verified
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    description=f"**Not Verified!**\n"
                                f"Run `/verify (ign)`")
                await interaction.edit_original_response(embed=embed)

            if guild_member in interaction.user.roles:  # Guild Roles
                uuid = discord_data['users'][str(interaction.user.id)]
                username = user_data['users'][uuid]
                sb_level = 0
                data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
                logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{username}")

                for profile in data['profiles']:
                    try:
                        level = data['profiles'][profile]['data']['skyblock_level']['levelWithProgress']
                        sb_level = level if level > sb_level else sb_level
                    except Exception as e:
                        logging.error(e)

                # if 240 <= sb_level < 280:
                #     roles_to_give.append(interaction.guild.get_role(BABY_BEE))
                # elif 280 <= sb_level < 320:
                #     roles_to_give.append(interaction.guild.get_role(TODDLER_BEE))
                # elif 320 <= sb_level < 360:
                #     roles_to_give.append(interaction.guild.get_role(SWEATY_BEE))
                # elif 360 <= sb_level:
                #     roles_to_give.append(interaction.guild.get_role(ULTIMATE_BEE))

            for role in roles_to_give:
                roles += f"{role.mention} "
                await interaction.user.add_roles(role)
                await asyncio.sleep(0.2)

            embed = discord.Embed(colour=discord.Colour.teal(), description="You already have all the roles!")
            if roles != "":
                embed.description = ("**Successfully Added Roles!**\n"
                                     f"**Roles:** {roles}")
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            logging.error(e)

async def setup(client):
    await client.add_cog(Roles(client))
