from fetch_data.fetch_data_cctx import fetch_l1_bbo
import time
import asyncio
import os
import json

with open("market-data-service\exchanges.json") as f:
    data=json.load(f)

async def get_and_push():
    with open("market-data-service\exchanges.json") as f:
        data=json.load(f)
    ma=data.get("ma")
    for i in ma:
        for j in ma[i]:
            print(i+" "+j)
            data=await fetch_l1_bbo(i,j)
            print(data)

async def main():
    while True:
        await get_and_push()
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())