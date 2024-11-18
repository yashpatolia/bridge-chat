import requests
import logging
import sqlite3


def get_uuid(username) -> str:
    with sqlite3.connect("temporals.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT uuid FROM users WHERE ign = ?", (username.lower(),))
        uuid = cursor.fetchone()

        if uuid:
            return uuid[0]

        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()['id']
        logging.info(f"GET https://api.mojang.com/users/profiles/minecraft/{username}")
        cursor.execute("INSERT INTO users (uuid, ign) VALUES (?, ?)", (uuid, username.lower()))
        connection.commit()
        return uuid
