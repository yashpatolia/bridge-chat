import requests
import logging

def get_skyblock_level(username) -> float:
    skyblock_level = 0
    data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{username}")

    for profile in data['profiles']:
        try:
            level = data['profiles'][profile]['data']['skyblock_level']['levelWithProgress']
            skyblock_level = level if level > skyblock_level else skyblock_level
        except Exception as e:
            logging.error(e)
    
    return skyblock_level