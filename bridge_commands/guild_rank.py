import time
import requests
import logging


def guild_rank_change(username, guild_rank, bot):
    guild_ranks = {'Member': 200, 'Past': 250, 'Pres': 300, 'Future': 350}
    if guild_rank not in guild_ranks.keys():
        bot.chat(f'/gc {username}: No rank change possible!')
        return f"{username}: No rank change possible!"

    data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{username}")
    skyblock_level = 0

    for profile in data['profiles']:
        try:
            level = data['profiles'][profile]['data']['skyblock_level']['levelWithProgress']
            skyblock_level = level if level > skyblock_level else skyblock_level
        except Exception as e:
            logging.error(e)

    required_rank = [rank for rank, level in guild_ranks.items() if level < skyblock_level][-1]
    required_rank_index = list(guild_ranks.keys()).index(required_rank)
    guild_rank_index = list(guild_ranks.keys()).index(guild_rank)

    if (required_rank_index - guild_rank_index) > 0:
        for i in range(required_rank_index - guild_rank_index):
            bot.chat(f'/g promote {username}')
            time.sleep(1)
        return f"Promoted {username} from {guild_rank} to {required_rank}"
    elif (required_rank_index - guild_rank_index) < 0:
        for i in range(guild_rank_index - required_rank_index):
            bot.chat(f'/g demote {username}')
            time.sleep(1)
        return f"Demoted {username} from {guild_rank} to {required_rank}"
    else:
        bot.chat(f'/gc {username}: No rank change required!')
        return f"{username}: No rank change required!"
