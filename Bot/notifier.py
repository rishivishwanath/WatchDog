import requests
from config import TOKEN
from db import get_users_by_pair

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_arbitrage_alert(pair, message):
    subs = get_users_by_pair(pair.lower())
    for user in subs:
        payload = {"chat_id": user["chat_id"], "text": message}
        requests.post(API_URL, data=payload)
