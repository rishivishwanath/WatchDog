import time
import json
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda v: v.encode('utf-8')
)

def get_and_push(data,i):
    ma=data.get("listed")
    for exchange in ma:
        for symbol in ma[exchange]:
            task = {
                "exchange": exchange,
                "symbol": symbol
            }
            key = f"{exchange}:{symbol}"
            i+=1
            print(f"[*] Sending task: {key}")
            producer.send("tasks", key=key, value=task)

def main():
    with open("exchanges.json") as f:
        data=json.load(f)
        i=0
    while True:
        get_and_push(data,i)
        time.sleep(10)

if __name__ == "__main__":
    main()