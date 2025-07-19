# For okx exchange:
# Template: wss://gomarket-api.goquant.io/ws/l1-orderbook/okx/{symbol}

# WebSocket L1 Orderbook Connection
import websockets
import asyncio
import json

async def connect():
    async with websockets.connect('wss://gomarket-api.goquant.io/ws/l1-orderbook/okx/') as ws:
        print("Connected to L1 Orderbook")
        
        while True:
            message = await ws.recv()
            print("Message:", json.loads(message))

asyncio.get_event_loop().run_until_complete(connect())