import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
    key_serializer=lambda v: v.encode('utf-8')
)

def send_data(data):
    topic=data['symbol'].replace('/', '_')
    print(topic)
    producer.send(topic,key=topic,value=data)