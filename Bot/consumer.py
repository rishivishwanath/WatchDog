from kafka import KafkaConsumer
import json
import asyncio
from db import get_subscribers_by_filters
import requests
from config import TOKEN

API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"  # Replace <YOUR_TOKEN> with actual bot token

def notify(pair, current_lot_size, current_percent, ask_exchange, bid_exchange):
    subscribers = get_subscribers_by_filters(pair, current_percent, current_lot_size)
    print(subscribers)
    for chat_id, _, _, _ in subscribers:  # You may ignore min_lot and min_percentage if not needed
        msg = (
            f"\U0001F4C8 <b>{pair}</b> triggered arbitrage alert!\n"
            f"🟢 <b>On:</b> {ask_exchange}\n"
            f"🔴 <b>On:</b> {bid_exchange}\n"
            f"📦 <b>Lot:</b> {current_lot_size:.6f}\n"
            f"📈 <b>Change:</b> {current_percent:.2f}%"
        )
        requests.post(API_URL, data={
            "chat_id": chat_id,
            "text": msg,
            "parse_mode": "HTML"
        })

def consume_kafka():
    consumer = KafkaConsumer(
        'arbitrage',
        bootstrap_servers='localhost:9092',
        auto_offset_reset='latest',
        group_id='telegram-bot-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        key_deserializer=lambda x: x.decode('utf-8') if x else None
    )

    for message in consumer:
        try:
            pair = message.key or message.value.get("symbol")  # fall back to symbol
            data = message.value

            ask_exchange = data.get("ask_exchange")
            bid_exchange = data.get("bid_exchange")
            symbol = data.get("symbol")
            lot = float(data.get("plausible_size", 0.0))
            ask = float(data.get("ask_price", 0.0))
            bid = float(data.get("bid_price", 0.0))

            if ask == 0:
                continue

            percent = round(((bid - ask) / ask) * 100, 2)

            # Call the alert function
            notify(pair, lot, percent, ask_exchange, bid_exchange)

        except Exception as e:
            print(f"[ERROR] Failed to process message: {e}")
