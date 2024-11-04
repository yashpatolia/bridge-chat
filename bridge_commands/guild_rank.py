import time
from utils.get_skyblock_level import get_skyblock_level


def guild_rank_change(username, guild_rank, bot):
    guild_ranks = {'Member': 200, 'Past': 250, 'Pres': 300, 'Future': 350}
    if guild_rank not in guild_ranks.keys():
        bot.chat(f'/gc {username}: No rank change possible!')
        return f"{username}: No rank change possible!"

    skyblock_level = get_skyblock_level(username)
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
