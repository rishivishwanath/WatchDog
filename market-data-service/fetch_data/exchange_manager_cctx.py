import ccxt.async_support as ccxt

exchange_clients = {}

async def init_exchange(exchange_id: str):
    """Initialize an exchange client if not already created."""
    if exchange_id not in exchange_clients:
        print(f"🔄 Initializing client for {exchange_id}")
        client = getattr(ccxt, exchange_id)({'enableRateLimit': True})
        await client.load_markets()
        exchange_clients[exchange_id] = client
    return exchange_clients[exchange_id]

async def get_exchange(exchange_id: str):
    """Retrieve an existing exchange client (initialize if missing)."""
    return await init_exchange(exchange_id)

async def close_all_exchanges():
    """Close all clients gracefully (on shutdown)."""
    for ex in exchange_clients.values():
        await ex.close()
    exchange_clients.clear()
