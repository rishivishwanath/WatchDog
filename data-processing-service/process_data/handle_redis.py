import json
import os
import redis.asyncio as aioredis
from dotenv import load_dotenv
load_dotenv()
import asyncio

r = aioredis.Redis(
    host='redis-19355.crce179.ap-south-1-1.ec2.redns.redis-cloud.com',
    port=19355,
    decode_responses=True,
    username="default",
    password=os.getenv("REDIS_PASSWORD"))

async def update_data(symbol, exchange=None, data=None):
    all_data = await r.hgetall(symbol)
    if all_data:
        formatted = {
            ex: json.loads(val) for ex, val in all_data.items()
        }
    else:
        print(f"⚠️ No data found for {symbol}")
    result= await asyncio.create_task(r.hset(symbol, exchange, json.dumps(data)))
    print(result)
    return [symbol,formatted]

async def main():
    await update_data("SOL/USDT")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
