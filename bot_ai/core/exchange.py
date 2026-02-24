# ============================================
# Path: C:\TradingBots\NT\bot_ai\core\exchange.py
# Purpose: Exchange client factory using CCXT and config loader
# Format: UTF-8 without BOM, production-ready
# ============================================

import ccxt
from bot_ai.config.config_loader import get_binance_credentials

def get_exchange_client(cfg):
    """
    Initialize and return a CCXT exchange client based on config.

    Parameters:
        cfg (dict): Configuration dictionary with exchange settings.

    Returns:
        ccxt.Exchange: Configured exchange client instance.
    """
    name = cfg.get("exchange", {}).get("name", "binance")
    testnet = cfg.get("exchange", {}).get("testnet", False)
    api_key, api_secret = get_binance_credentials()

    if name == "binance":
        client = ccxt.binance({
            "apiKey": api_key,
            "secret": api_secret,
            "enableRateLimit": True,
        })

        if testnet:
            client.set_sandbox_mode(True)
            client.urls["api"] = "https://testnet.binance.vision/api"

        return client

    raise ValueError(f"Неизвестная биржа: {name}")
