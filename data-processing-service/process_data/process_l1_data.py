import asyncio
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from message_queue.put_l1_arbitrage import send_data
from .handle_redis import update_data

market_data = {}

async def process_l1_bbo(exchange:str,symbol:str,bid_price:float,bid_size:float,ask_price:float,ask_size:float,timestamp:str):
    if symbol not in market_data:
        market_data[symbol] = {}
    cleandata = {
        'bid_price':bid_price,
        'bid_size': bid_size,
        'ask_price':ask_price,
        'ask_size':ask_size
    }
    all_exchange_data=await update_data(symbol, exchange, cleandata)
    print(f"📈 Processed {symbol} on {all_exchange_data}")
    market_data[symbol][exchange] = {'bid_price': bid_price,'bid_size':bid_size,'ask_price': ask_price ,'ask_size':ask_size, 'timestamp': timestamp}
    asyncio.create_task(compare(bid_price,ask_price,symbol,exchange, bid_size,ask_size))
    

async def compare(bid_price:float,ask_price:float,symbol:str, exchange_prior:str,bid_size:float,ask_size:float,timestamp:str=None):
    for exchange, data in market_data[symbol].items():
        if data['bid_price'] > 1.0001*ask_price:
            plausible_size= min(data['bid_size'], ask_size)
            # print(f"Arbitrage opportunity detected for {symbol} on {exchange} and {exchange_prior}: Bid {data['bid_price']} > Ask {ask_price} for {plausible_size} lots" )
            asyncio.to_thread(send_data(exchange_prior,exchange,symbol,data['bid_price'],ask_price,plausible_size,timestamp))
        elif data['ask_price']*1.0001 < bid_price:
            plausible_size= min(data['ask_size'], bid_size)
            # print(f"Arbitrage opportunity detected for {symbol} on {exchange} and {exchange_prior}: Ask {data['ask_price']} < Bid {bid_price} for {min(data['ask_size'],bid_size)} lots")   
            asyncio.to_thread(send_data(exchange,exchange_prior,symbol,bid_price,data['ask_price'],plausible_size,timestamp))
