import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE

class Guild(commands.GroupCog, name="guild"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="list", description="Lists guild members!")
    async def list(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        self.client.bot.chat("/g list")
        await asyncio.sleep(0.75)
        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(), description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="online", description="Online guild members!")
    async def online(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()

        self.client.bot.chat("/g online")
        await asyncio.sleep(0.75)
        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(), description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)

    @app_commands.command(name="mute", description="Mutes a guild member")
    @app_commands.describe(ign="Enter an IGN")
    @app_commands.describe(time="Time for the mute (m, h, d)")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def mute(self, interaction: discord.Interaction, ign: str, time: str) -> None:
        self.client.bot.chat(f"/g mute {ign} {time}")
        embed = discord.Embed(colour=discord.Colour.green(), description=f"**Muted:** {ign} for {time}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="unmute", description="Unmutes a guild member")
    @app_commands.describe(ign="Enter an IGN")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def unmute(self, interaction: discord.Interaction, ign: str) -> None:
        self.client.bot.chat(f"/g unmute {ign}")
        embed = discord.Embed(colour=discord.Colour.green(), description=f"**Unmuted:** {ign}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="invite", description="Invites a member")
    @app_commands.describe(ign="Enter name to invite to the guild")
    @app_commands.checks.has_role(STAFF_ROLE)
    async def invite(self, interaction: discord.Interaction, ign: str) -> None:
        self.client.bot.chat(f"/g invite {ign}")
        embed = discord.Embed(colour=discord.Colour.green(), description=f"**Invited:** {ign}")
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(Guild(client))
