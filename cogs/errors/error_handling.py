import discord
from discord import app_commands
from discord.ext import commands

class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    def cog_load(self):  # attaching the handler when the cog is loaded and storing the old handler
        tree = self.client.tree
        self._old_tree_error = tree.on_error
        tree.on_error = self.tree_on_error

    @commands.Cog.listener()
    async def tree_on_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingRole):
            await interaction.response.send_message("You don't have the required role.", ephemeral=True)

async def setup(client):
    await client.add_cog(ErrorHandling(client))