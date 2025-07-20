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


if __name__ == "__main__":
    symbol = 'BTC/USDT'
    data = fetch_l1_bbo('binance', symbol)
    print(f"time:{data['timestamp']} Best Bid: {data['bid_price']} | Best Ask: {data['ask_price']}")
