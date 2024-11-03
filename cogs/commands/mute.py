import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE


class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="mute", description="Mutes a guild member")
    @app_commands.describe(ign="Enter an IGN")
    @app_commands.describe(time="Time for the mute (m, h, d)")
    async def mute(self, interaction: discord.Interaction, ign: str, time: str):
        await interaction.response.defer()
        staff_role = interaction.guild.get_role(STAFF_ROLE)
        if staff_role not in interaction.user.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="Not sufficient permissions!")
        else:
            self.client.bot.chat(f"/g mute {ign} {time}")
            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"**Muted:** {ign} for {time}")
        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Mute(client))
