import ccxt
import asyncio
import time
from datetime import datetime, timezone
import ccxt.async_support as ccxt  # Async version of ccxt
from .exchange_manager_cctx import get_exchange

async def fetch_l1_bbo(exchange_id: str, symbol: str) -> dict:
    exchange = await get_exchange(exchange_id)
    await exchange.load_markets()
    
    orderbook = await exchange.fetch_order_book(symbol)
    bid = orderbook['bids'][0] if orderbook['bids'] else [None, None]
    ask = orderbook['asks'][0] if orderbook['asks'] else [None, None]
    return {
        'exchange': exchange_id,
        'symbol': symbol,
        'bid_price': bid[0],
        'bid_size': bid[1],
        'ask_price': ask[0],
        'ask_size': ask[1],
        'timestamp': datetime.now(timezone.utc),
        'datetime': orderbook.get('datetime'),
    }

def fetch_l2_orderbook(exchange_id: str, symbol: str, depth: int = 10) -> dict:
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,
    })
    exchange.load_markets()
    orderbook = exchange.fetch_order_book(symbol, limit=depth)
    
    return {
        'exchange': exchange_id,
        'symbol': symbol,
        'bids': orderbook['bids'],  
        'asks': orderbook['asks'],
        'timestamp': datetime.now(timezone.utc),
        'datetime': orderbook.get('datetime'),
    }

def fetch_ohlcv_data(exchange_id: str, symbol: str, timeframe: str = '1m', limit: int = 100) -> dict:
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,
    })
    exchange.load_markets()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    return {
        'exchange': exchange_id,
        'symbol': symbol,
        'timeframe': timeframe,
        'ohlcv': [
            {'timestamp': entry[0], 'open': entry[1], 'high': entry[2],
             'low': entry[3], 'close': entry[4], 'volume': entry[5]}
            for entry in ohlcv
        ],
    }

async def main():
    start_time = time.perf_counter()
    
    tasks = [
        fetch_l1_bbo("binance", "BTC/USDT"),
        fetch_l1_bbo("bybit", "BTC/USDT"),
        fetch_l1_bbo("okx", "BTC/USDT"),
    ]
    
    results = await asyncio.gather(*tasks)
    
    end_time = time.perf_counter()
    print(f"\nExecution time: {end_time - start_time:.2f} seconds\n")
    
    for r in results:
        print(r)

if __name__ == "__main__":
    asyncio.run(main())