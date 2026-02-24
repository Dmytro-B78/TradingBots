# ============================================
# File: bot_ai/selector/filters.py
# Purpose: Binance client init + pair filters
# ============================================

import ccxt
import logging
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

def get_exchange_client(cfg):
    name = cfg["exchange"]["name"]
    testnet = cfg["exchange"].get("testnet", False)

    api_key = os.environ.get("BINANCE_API_KEY")
    api_secret = os.environ.get("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ValueError("BINANCE_API_KEY or BINANCE_API_SECRET missing in .env")

    if name.lower() == "binance":
        exchange_class = getattr(ccxt, "binance")
        params = {
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        }
        if testnet:
            params["urls"] = {
                "api": {
                    "public": "https://testnet.binance.vision/api",
                    "private": "https://testnet.binance.vision/api",
                }
            }
        client = exchange_class(params)
        logging.debug(f"[EXCHANGE] Binance client initialized (testnet={testnet})")

        try:
            ping = client.fetch_status()
            logging.debug(f"[EXCHANGE] API status: {ping.get('status')}")
        except Exception as e:
            logging.error(f"[EXCHANGE] API connection error: {e}")

        return client

    raise ValueError(f"Unknown exchange: {name}")

def filter_by_volume(pairs, min_volume):
    return [p for p in pairs if p.get("volume", 0) >= min_volume]

def filter_by_spread(pairs, max_spread):
    return [p for p in pairs if p.get("spread", 0) <= max_spread]

def filter_by_volatility(pairs, min_volatility):
    return [p for p in pairs if p.get("volatility", 0) >= min_volatility]

def filter_by_whitelist(pairs, whitelist):
    return [p for p in pairs if p["symbol"] in whitelist]
