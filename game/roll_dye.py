import random
import logging
import sqlite3
import discord
import time
from utils.get_uuid import get_uuid
from config import DYE_DROPS_CHANNEL, BRIDGE_CHANNEL


def roll_dye(username, bot) -> None:
    uuid = get_uuid(username)
    bridge_webhook = discord.SyncWebhook.from_url(BRIDGE_CHANNEL)
    dye_webhook = discord.SyncWebhook.from_url(DYE_DROPS_CHANNEL)

    with sqlite3.connect("temporals.db") as connection:
        cursor = connection.cursor()
        connection.execute("PRAGMA foreign_keys = ON;")
        cursor.execute("SELECT dye_id, weight FROM dyes")
        results = cursor.fetchall()

        dye_ids, weights = zip(*results)
        loot_id = random.choices(list(dye_ids), weights=list(weights), k=1)[0]

        cursor.execute("SELECT received FROM users_dyes WHERE dye_id = ? AND uuid = ?", (loot_id, uuid))
        obtained = cursor.fetchone()[0]
        logging.info(f"{username} rolled {loot_id} (Obtained: {obtained})")

        if loot_id != "nothing" and obtained == 0:
            cursor.execute("SELECT dye_name, weight, hex FROM dyes WHERE dye_id = ?", (loot_id,))
            dye_name, weight, hex_color = cursor.fetchone()
            cursor.execute("UPDATE users_dyes SET received = TRUE WHERE dye_id = ? AND uuid = ?", (loot_id,uuid))

            logging.warning(f"{username} unlocked {dye_name}!")
            time.sleep(0.5)
            bot.chat(f'/gc DYE DROP: {username} found {dye_name} (1/{round(100/weight)})!')
            embed = discord.Embed(color=discord.Color.from_str(f"#{hex_color.lower()}"), title=username,
                                  description=f"Unlocked **{dye_name}** (1/{round(100/weight)})!\n")
            bridge_webhook.send(embed=embed)
            dye_webhook.send(embed=embed)
        connection.commit()
