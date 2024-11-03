import logging
import re
import discord
import asyncio
import emoji
from datetime import datetime
from discord.ext import commands
from javascript import On
from config import OPTIONS, BRIDGE_CHANNEL, BRIDGE_CHANNEL_ID, OFFICER_CHANNEL, OFFICER_CHANNEL_ID
from bridge_commands.bridge_commands import bridge_commands


class Bridge(commands.Cog):
    def __init__(self, client):
        self.client = client

        @On(self.client.bot, "chat")
        def handle_message(this, username, message, *args):
            bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_CHANNEL)
            officer_webhook = discord.SyncWebhook.from_url(OFFICER_CHANNEL)

            embed = discord.Embed(
                color=discord.Color.blue(),
                timestamp=datetime.now())

            if username in ["Guild", "Officer"]:
                if message.split(' ')[-1] in ["joined.", "left."]:
                    embed = discord.Embed()
                    embed.colour = discord.Color.green() if message.split(' ')[-1] == "joined." else discord.Color.red()
                    embed.description = message
                    bridge_webhook.send(embed=embed)
                    return

                try:
                    state = username
                    match = re.search(r"^(?:\[(?P<rank>.+?)\])?\s?(?P<player>.+?)\s?(?:\[(?P<guild_rank>.+?)\])?: (?P<message>.*)$", message)
                    message = re.sub('@', '', match.group('message'))
                    username = match.group("player")
                    guild_rank = match.group("guild_rank")

                    if username == OPTIONS['username']:
                        return

                    if message.split(' ')[0][0] == ".":  # Bot Commands
                        text = bridge_commands(message, username, guild_rank, self.client.bot)
                        bridge_webhook.send(text)

                    embed.set_author(name=f"{username}", icon_url=f"https://mc-heads.net/avatar/{username}")
                    embed.description = message
                    embed.set_footer(text=f"{guild_rank}")

                    logging.info(f'[MC] {username}: {message}')
                    if state == "Guild":
                        bridge_webhook.send(embed=embed)
                    elif state == "Officer":
                        officer_webhook.send(embed=embed)
                except Exception as e:
                    logging.error(e)
                    return

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if len(message.content) > 0 and (str(message.channel.id) in [str(BRIDGE_CHANNEL_ID), str(OFFICER_CHANNEL_ID)]):  # Messages
            await asyncio.sleep(0.1)
            logging.info(f'[D] {message.author.display_name} {message.content}')

            message.content = emoji.demojize(discord.utils.remove_markdown(message.clean_content))

            if message.type == discord.MessageType.reply:  # Replies
                reply_message = await message.channel.fetch_message(message.reference.message_id)
                message.content = f"{message.author.display_name} replied to {reply_message.author.display_name}: {message.content}"
            else:
                message.content = f"{message.author.display_name}: {message.content}"

            if str(message.channel.id) == str(BRIDGE_CHANNEL_ID):
                self.client.bot.chat(f'/gc {message.content}')
            elif str(message.channel.id) == str(OFFICER_CHANNEL_ID):
                self.client.bot.chat(f'/oc {message.content}')

        for attachment in message.attachments:  # Attachments
            await asyncio.sleep(0.5)
            logging.info(f"[D] {message.author.display_name}: {attachment.url.split('?')[0]}")

            if str(message.channel.id) == str(BRIDGE_CHANNEL_ID):
                self.client.bot.chat(f'/gc {message.author.display_name}: {attachment.url.split("?")[0]}')
            elif str(message.channel.id) == str(OFFICER_CHANNEL_ID):
                self.client.bot.chat(f'/oc {message.author.display_name}: {attachment.url.split("?")[0]}')


async def setup(client):
    await client.add_cog(Bridge(client))
