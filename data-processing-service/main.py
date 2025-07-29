import asyncio
import json
from aiokafka import AIOKafkaConsumer

async def process_message(message):
    print(f"[{message.topic}] {message.value}")

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
            # Schedule message processing concurrently
            asyncio.create_task(process_message(message))
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
