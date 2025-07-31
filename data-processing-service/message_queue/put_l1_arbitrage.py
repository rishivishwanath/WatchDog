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

def send_data(ask_exchange,bid_exchange,symbol,bid_price,ask_price,plausible_size,timestamp):
    data= {
        "ask_exchange": ask_exchange,
        "bid_exchange": bid_exchange,
        "symbol": symbol,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "plausible_size": plausible_size,
        "timestamp": timestamp
    }
    future = producer.send("arbitrage", key=symbol, value=data)
    future.add_callback(lambda meta: print(f"✅ Delivered: {meta.topic}-{meta.partition}"))
    future.add_errback(lambda exc: print(f"❌ Delivery failed: {exc}"))