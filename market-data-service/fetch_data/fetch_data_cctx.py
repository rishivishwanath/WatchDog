from datetime import datetime, timezone
import ccxt

def fetch_l1_bbo(exchange_id: str, symbol: str) -> dict:
    exchange = getattr(ccxt, exchange_id)({
        'enableRateLimit': True,
    })
    exchange.load_markets()
    orderbook = exchange.fetch_order_book(symbol)  # REST polling
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

if __name__ == "__main__":
    data = fetch_ohlcv_data('binance', 'BTC/USDT', '1d', limit=100)
    latest = data['ohlcv'][-1]
    print(f"[{data['exchange']} {data['symbol']} {data['timeframe']}] "
            f"Latest Candle: O={latest['open']} H={latest['high']} "
            f"L={latest['low']} C={latest['close']} V={latest['volume']}")
