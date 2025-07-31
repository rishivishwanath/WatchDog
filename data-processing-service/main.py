import asyncio
import json
from aiokafka import AIOKafkaConsumer
from process_data.process_l1_data import process_l1_bbo
from process_data.handle_redis import update_data

async def process_data(message):
    # print(f"[{message.topic}] {message.value}")

    await process_l1_bbo(message.value['exchange'],
                          message.value['symbol'],
                          message.value['bid_price'],
                          message.value['bid_size'],
                          message.value['ask_price'],
                          message.value['ask_size'],
                          message.value['timestamp'])
    cleandata = {
        'bid_price': message.value['bid_price'],
        'bid_size': message.value['bid_size'],
        'ask_price': message.value['ask_price'],
        'ask_size': message.value['ask_size']
    }
    await update_data(message.value['symbol'],
                      message.value['exchange'],
                        cleandata)



async def consume_messages():
    consumer = AIOKafkaConsumer(
        'data',
        bootstrap_servers='localhost:9092',
        group_id='process-data-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    try:
        async for message in consumer:
            asyncio.create_task(process_data(message))
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
