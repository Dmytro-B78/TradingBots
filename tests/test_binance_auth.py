# File: C:\TradingBots\NT\tests\test_binance_auth.py
# Purpose: Validate .env credentials and connectivity to Binance Testnet
# Structure: Load .env → Initialize client → Attempt get_account() → Print result
# Encoding: UTF-8 without BOM

from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

try:
    account_info = client.get_account()
    print("✅ SUCCESS: Connected to Binance Testnet.")
    print("Account info:", account_info)
except Exception as e:
    print("❌ ERROR:", e)
