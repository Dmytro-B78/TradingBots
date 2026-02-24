# ============================================
# File: C:\TradingBots\NT\binance_client.py
# Purpose: Force .env loading and log actual API key used
# ============================================

from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="C:/TradingBots/NT/.env")

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")

print(">>> Loaded API key:", api_key)

client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

def place_order(symbol, side, quantity):
    print("=== ORDER REQUEST ===")
    print({
        "symbol": symbol,
        "side": side,
        "type": "MARKET",
        "quantity": quantity
    })

    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        print("=== ORDER RESPONSE ===")
        print(order)
        return order
    except BinanceAPIException as e:
        print("=== ORDER FAILED ===")
        print("Status Code:", e.status_code)
        print("Error Code:", e.code)
        print("Message:", e.message)
        return None
    except Exception as e:
        print("=== ORDER EXCEPTION ===")
        print(type(e), e)
        return None
