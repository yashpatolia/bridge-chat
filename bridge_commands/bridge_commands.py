from bridge_commands.guild_rank import guild_rank_change
from utils.get_skyblock_level import get_skyblock_level
from utils.get_networth import get_networth
from utils.sql_eval import sql_eval


def bridge_commands(message, username, guild_rank, bot):
    text = ""
    message = message.lower()

    if message.split(' ')[0] in ['.bridge', '.help']:  # Help
        text = '.help'
        bot.chat(f'/gc {username}: '
                 f'.rankup - '
                 f'.level (ign) - '
                 f'.networth (ign)')
    elif message.split(' ')[0] in ['.updaterank', '.upgraderank', '.rankup', ".demote", ".derank"]:  # Rankup
        text = guild_rank_change(username, guild_rank, bot)
    elif message.split(' ')[0] in ['.level', '.lvl', '.sblevel']:  # Skyblock Level
        if len(message.split(' ')) > 1:
            username = message.split(' ')[1]
        skyblock_level = get_skyblock_level(username)
        bot.chat(f'/gc {username}: Highest Skyblock Level - {skyblock_level}')
        return f"{username}'s Highest Skyblock Level - {skyblock_level}"
    elif message.split(' ')[0] in ['.nw', '.networth']:  # Networth
        if len(message.split(' ')) > 1:
            username = message.split(' ')[1]
        networth = get_networth(username)
        bot.chat(f'/gc {username}: Highest Networth - {networth}')
        return f"{username}'s Highest Networth: {networth}"

    elif message.split(' ')[0] in ['.db']:  # DB Eval
        if username.lower() != 'seazyns':
            return 'Not authorized'

        results = sql_eval(message.sub('.db ', ''))
        bot.chat(f'/gc {username}: {results}')
        return f"{username}: {results}"

    return text
