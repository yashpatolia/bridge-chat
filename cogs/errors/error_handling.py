import discord
from discord import app_commands
from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("You don't have the required role.", ephemeral=True)

async def setup(client):
    await client.add_cog(ErrorHandling(client))