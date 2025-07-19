# Get Orderbook Data
import requests

response = requests.get(
    'https://gomarket-api.goquant.io/api/l1-orderbook/okx/USDT-SGD')

result = response.json()
print(result)