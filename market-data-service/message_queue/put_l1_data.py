import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    linger_ms=5,
    batch_size=32768,
    # compression_type='lz4',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
    key_serializer=lambda v: v.encode('utf-8')
)

def send_data(data):
    symbol_key = data['symbol']
    future = producer.send("data", key=symbol_key, value=data)
    future.add_callback(lambda meta: print(f"✅ Delivered: {meta.topic}-{meta.partition}"))
    future.add_errback(lambda exc: print(f"❌ Delivery failed: {exc}"))