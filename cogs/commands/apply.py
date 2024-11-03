import discord
from discord.ext import commands
from discord import app_commands
from config import GUILD_NAME, STAFF_ROLE


class Apply(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="apply", description=f"Apply for {GUILD_NAME} Guild")
    @app_commands.describe(ign="Minecraft Username")
    async def exec(self, interaction: discord.Interaction, ign: str):
        await interaction.response.defer()

        app_category = discord.utils.get(interaction.guild.categories, name="applications")
        staff_role = interaction.guild.get_role(STAFF_ROLE)
        overwrites = {interaction.user: discord.PermissionOverwrite(read_messages=True),
                      interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                      staff_role: discord.PermissionOverwrite(read_messages=True)}
        app_channel = await interaction.guild.create_text_channel(f'{ign.lower()}-app', category=app_category, overwrites=overwrites)

        embed = discord.Embed(
            colour=discord.Colour.dark_red(),
            description=f"Created Application Ticket: {app_channel.mention}")

        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Apply(client))
