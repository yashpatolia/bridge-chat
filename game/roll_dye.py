import random
import logging
import json
from commands.game.get_uuid import get_uuid


def roll_rng(username, bot):
    text = ""
    with open('drops.json', 'r') as file:
        drops = json.load(file)

    with open('data.json', 'r') as file:
        data = json.load(file)

    with open('users.json', 'r') as file:
        users = json.load(file)

    uuid = get_uuid(username)

    if uuid in data['users'].keys():
        loot = random.choices(list(drops.keys()), weights=list(drops.values()), k=1)[0]
        logging.warning(f"{username} rolled {loot}!")

        if loot != "Nothing":
            if loot in list(data['users'][uuid]['inventory'].keys()):
                amount = data['users'][uuid]['inventory'][loot]
                data['users'][uuid]['inventory'][loot] = amount + 1
            else:
                data['users'][uuid]['inventory'][loot] = 1

            with open('data.json', 'w') as file:
                file.write(json.dumps(data, indent=4))

            bot.chat(f'/gc {username}: Found {loot}!')
            text = f"{username}: Found {loot}!"

    return text
