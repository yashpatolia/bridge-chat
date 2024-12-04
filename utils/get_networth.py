import requests
import logging

def get_networth(username) -> str:
    networth_amount = 0
    data = requests.get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    logging.info(f"GET https://sky.shiiyu.moe/api/v2/profile/{username}")

    for profile in data['profiles']:
        try:
            amount = data['profiles'][profile]['data']['networth']['networth']
            purse = data['profiles'][profile]['data']['networth']['purse']
            bank = data['profiles'][profile]['data']['networth']['bank']
            personal_bank = data['profiles'][profile]['data']['networth']['personalBank']
            total = amount + purse + bank + personal_bank
            networth_amount = total if total > networth_amount else networth_amount
        except Exception as e:
            logging.error(e)

    networth_amount = float('{:.4g}'.format(networth_amount))
    magnitude = 0
    while abs(networth_amount) >= 1000:
        magnitude += 1
        networth_amount /= 1000.0
    networth_amount = '{}{}'.format('{:f}'.format(networth_amount).rstrip('0').rstrip('.'),
                                    ['', 'K', 'M', 'B', 'T'][magnitude])
    
    return networth_amount