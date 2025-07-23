from kafka import KafkaConsumer
import json
from fetch_data.fetch_data_cctx import fetch_l1_bbo
from message_queue.put_l1_data import send_data
# Connect to the broker running in Docker (use 'localhost:9092' from the host machine)
consumer = KafkaConsumer(
    'tasks',                        # Topic name
    bootstrap_servers=['localhost:9092'], # From host machine
    group_id='fetch-data-group',          # Consumer group for parallelism and checkpointing
    auto_offset_reset='earliest',         # Start from earliest if no committed offset
    enable_auto_commit=True,              # Kafka handles offset commits
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Expecting JSON messages
)
def handle_tasks():
    for message in consumer:
        print(f"[{message.topic}] {message.value}")
        data=fetch_l1_bbo(message.value['exchange'],message.value['symbol'])
        send_data(data)

if __name__=="__main__":
    handle_tasks()