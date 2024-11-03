import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE


class Invite(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="invite", description="Invites a member")
    @app_commands.describe(ign="Enter name to invite to the guild")
    async def invite(self, interaction: discord.Interaction, ign: str):
        await interaction.response.defer()

        staff_role = interaction.guild.get_role(STAFF_ROLE)
        if staff_role not in interaction.user.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                description="Not sufficient permissions!")
        else:
            self.client.bot.chat(f"/g invite {ign}")
            embed = discord.Embed(
                colour=discord.Colour.green(),
                description=f"**Invited:** {ign}")
        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Invite(client))
