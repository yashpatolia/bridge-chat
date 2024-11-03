import logging
import discord
from discord.ext import commands
from discord import SyncWebhook
from javascript import On
from config import BRIDGE_CHANNEL, LOGS_CHANNEL, OPTIONS, GUILD_NAME


class MessageHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

        @On(self.client.bot, "messagestr")
        def messagestr(this, message, *args):
            logging.debug(f'[MC] {message}')
            bridge_webhook = SyncWebhook.from_url(BRIDGE_CHANNEL)
            logs_webhook = SyncWebhook.from_url(LOGS_CHANNEL)

            if "Online Members:" in message and self.client.save_guild_list is True:  # LOG Guild Online / List
                self.client.guild_list.append(message)
                self.client.save_guild_list = False
            if self.client.save_guild_list is True:
                self.client.guild_list.append(message)
            if f"Guild Name: {GUILD_NAME}" in message:
                self.client.save_guild_list = True

            if OPTIONS['username'].lower() in message.lower():
                return

            if message.lower().startswith("you cannot say the same message twice!"):
                embed = discord.Embed(
                    colour=discord.Colour.red(),
                    description="**You cannot send the same message twice!**")
                bridge_webhook.send(embed=embed)

            if message.lower().endswith("not found."):
                embed = discord.Embed(colour=discord.Colour.red(), description=f"{message}")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if 'was promoted from' in message.lower() or 'was demoted from' in message.lower():
                embed = discord.Embed(colour=discord.Colour.teal(), description=f"{message}")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if 'is already in another guild!' in message.lower():
                embed = discord.Embed(colour=discord.Colour.red(), description=f"{message}")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if 'was invited to the' in message.lower():
                embed = discord.Embed(colour=discord.Colour.orange(), description=f"{message}")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if "you invited" in message.lower() and "to your guild" in message.lower():
                embed = discord.Embed(colour=discord.Colour.orange(), description=f"{message}")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if "joined the guild!" in message.lower():
                embed = discord.Embed(colour=discord.Colour.green(), description=f"**{message}**")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if "left the guild!" in message.lower():
                embed = discord.Embed(colour=discord.Colour.red(), description=f"**{message}**")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)

            if "has muted" in message.lower() and "for" in message.lower():
                embed = discord.Embed(colour=discord.Colour.red(), description=f"**{message}**")
                bridge_webhook.send(embed=embed)
                logs_webhook.send(embed=embed)


async def setup(client):
    await client.add_cog(MessageHandler(client))
