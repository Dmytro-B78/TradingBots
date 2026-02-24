# ============================================
# File: C:\TradingBots\NT\bot_ai\execution\binance_executor.py
# Purpose: Order execution via Binance Testnet API with full diagnostics
# Structure: place_order with request/response logging
# Encoding: UTF-8 without BOM
# ============================================

import logging
from binance.client import Client
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE_API_SECRET")
client = Client(api_key, api_secret)
client.API_URL = "https://testnet.binance.vision/api"

def place_order(symbol: str, side: str, quantity: float):
    try:
        logging.debug(f"Placing order: symbol={symbol}, side={side}, quantity={quantity}")
        order = client.create_order(
            symbol=symbol,
            side=side.upper(),
            type="MARKET",
            quantity=quantity
        )
        logging.debug(f"Order response: {order}")
        return order
    except Exception as e:
        logging.error(f"[ERROR] Order failed: {e}")
        logging.debug(f"Exception repr: {repr(e)}")
        logging.debug(f"Exception args: {e.args}")
        return None
