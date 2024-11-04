import discord
import asyncio
import logging
from discord.ext import commands
from discord import app_commands
from config import OPTIONS, STAFF_ROLE
from javascript import require

mineflayer = require('mineflayer')


class Relog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="relog", description="Relogs the bridge bot")
    async def relog(self, interaction: discord.Interaction):
        await interaction.response.defer()

        staff_role = interaction.guild.get_role(STAFF_ROLE)
        if staff_role not in interaction.user.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="Not sufficient permissions!")
            await interaction.edit_original_response(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.orange(),
                description=f"**Relogging:** {OPTIONS['username']} in 5 seconds!")
            await interaction.edit_original_response(embed=embed)

            logging.info(f"[Relogging] {OPTIONS['username']} in 5 seconds!")
            self.client.reason = "relog"
            self.client.bot.end()
            await asyncio.sleep(5)
            await self.client.start_mineflayer(restart=True)


async def setup(client):
    await client.add_cog(Relog(client))
