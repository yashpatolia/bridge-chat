import discord
import asyncio
import logging
from discord.ext import commands
from javascript import Once, On
from config import OPTIONS, BRIDGE_CHANNEL


class Connections(commands.Cog):
    def __init__(self, client):
        self.client = client
    
        @Once(self.client.bot, "spawn")
        def spawn(this):
            logging.info(f"[Bot] Logged In")

            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_CHANNEL)
            embed = discord.Embed(
                title="Bridge Online",
                description=f"`Connected to {OPTIONS['host']}`",
                color=discord.Color.green())
            bridge_webhook.send(embed=embed)

        @On(self.client.bot, "end")
        def end(this, event):
            if self.client.reason == "relog":
                return

            logging.info(f"[Bot] Disconnected")
            
            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_CHANNEL)
            embed = discord.Embed(
                description=f"**Disconnected from `{OPTIONS['host']}`**\nRestarting **{OPTIONS['username']}** in 5 seconds!",
                color=discord.Color.orange())
            bridge_webhook.send(embed=embed)

            async def reconnect():
                await asyncio.sleep(5)
                await self.client.start_mineflayer(restart=True)
            asyncio.run(reconnect())


async def setup(client):
    await client.add_cog(Connections(client))
