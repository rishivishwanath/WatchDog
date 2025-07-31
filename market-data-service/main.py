import asyncio
import json
from aiokafka import AIOKafkaConsumer
from fetch_data.fetch_data_cctx import fetch_l1_bbo
from message_queue.put_l1_data import send_data
from fetch_data.exchange_manager_cctx import close_all_exchanges

async def process_message(message):
    """Process each Kafka message asynchronously."""
    print(f"[{message.topic}] {message.value}")
    data = await fetch_l1_bbo(message.value['exchange'], message.value['symbol'])
    send_data(data)

async def consume_messages():
    consumer = AIOKafkaConsumer(
        'tasks',
        bootstrap_servers='localhost:9092',
        group_id='fetch-data-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    await consumer.start()
    try:
        async for message in consumer:
            # Schedule message processing concurrently
            asyncio.create_task(process_message(message))
    except Exception as e:
        print(f"Error while consuming messages: {e}")
    finally:
        await close_all_exchanges()
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume_messages())
