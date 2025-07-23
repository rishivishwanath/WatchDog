from kafka import KafkaConsumer
import json

# Connect to the broker running in Docker (use 'localhost:9092' from the host machine)
consumer = KafkaConsumer(
    'tasks',                        # Topic name
    bootstrap_servers=['localhost:9092'], # From host machine
    group_id='fetch-data-group',          # Consumer group for parallelism and checkpointing
    auto_offset_reset='earliest',         # Start from earliest if no committed offset
    enable_auto_commit=True,              # Kafka handles offset commits
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))  # Expecting JSON messages
)

print("Listening for messages...")

for message in consumer:
    print(f"[{message.topic}] {message.value}")
