import requests

TOKEN = "7574106195:AAFqBNSAeWZ7Bgc5FV2AA7WPb5ThVUvjRzA"
url = f"https://api.telegram.org/bot{TOKEN}/getMe"

try:
    response = requests.get(url)
    data = response.json()
    
    if data['ok']:
        bot = data['result']
        print(f"🤖 Bot Name: {bot['first_name']}")
        print(f"👤 Username: @{bot['username']}")
        print(f"🆔 Bot ID: {bot['id']}")
        print(f"\n📱 How to find your bot:")
        print(f"1. Open Telegram")
        print(f"2. Search for: @{bot['username']}")
        print(f"3. Or click this link: https://t.me/{bot['username']}")
        print(f"4. Click 'START' to begin chatting!")
    else:
        print("❌ Error getting bot info")
        
except Exception as e:
    print(f"❌ Error: {e}")