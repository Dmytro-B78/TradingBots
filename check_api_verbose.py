import os
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

print("API KEY:", api_key)
print("API SECRET:", api_secret)

client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

try:
    account_info = client.get_account()
    print("✅ API key is valid. Account info:")
    print(account_info)
except Exception as e:
    print("❌ API key check failed:")
    print(type(e), e)
