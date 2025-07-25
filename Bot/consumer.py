from kafka import KafkaConsumer
import json
import asyncio
from notifier import send_arbitrage_alert  # We'll create this next

consumer = KafkaConsumer(
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    group_id='telegram-bot-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Subscribe to all arbitrage topics
consumer.subscribe(pattern='.*')

async def consume_kafka():
    loop = asyncio.get_running_loop()
    for message in consumer:
        topic = message.topic
        payload = message.value

        # You can enrich the message as needed
        msg = (
            f"📈 Arbitrage Alert for {topic.upper()}!\n"
            f"Price Difference: {payload.get('price_diff', '?')}\n"
            f"Exchanges: {payload.get('ex1', '?')} ↔ {payload.get('ex2', '?')}"
        )

        asyncio.run_coroutine_threadsafe(
            send_arbitrage_alert(topic, msg),
            loop
        )
