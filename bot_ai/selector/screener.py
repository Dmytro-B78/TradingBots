# ================================================================
# NT-Tech Screener (Diagnostic Version)
# File: bot_ai/selector/screener.py
# Purpose: Filter pairs by spread and print diagnostics.
# ASCII-only
# ================================================================

import json
import os
import requests

CONFIG_PATH = "C:/TradingBots/NT/config.json"


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError("config.json not found")

    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def fetch_ticker(symbol: str):
    url = f"https://api.binance.com/api/v3/ticker/bookTicker?symbol={symbol}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None


def compute_spread_pct(ticker):
    try:
        bid = float(ticker["bidPrice"])
        ask = float(ticker["askPrice"])
        if bid <= 0 or ask <= 0:
            return 999.0
        return (ask - bid) / bid * 100.0
    except Exception:
        return 999.0


def screen_pairs():
    cfg = load_config()

    all_pairs = cfg.get("selector", {}).get("all_pairs", [])
    max_spread_pct = cfg.get("metrics", {}).get("max_spread_pct", 0.30)

    screened = []

    print("=== Screener Diagnostics ===")

    for symbol in all_pairs:
        ticker = fetch_ticker(symbol)
        if ticker is None:
            print(f"{symbol}: ticker=None -> skip")
            continue

        spread_pct = compute_spread_pct(ticker)

        print(f"{symbol}: bid={ticker['bidPrice']} ask={ticker['askPrice']} spread={spread_pct:.4f}%")

        if spread_pct > max_spread_pct:
            print(f"{symbol}: spread too high -> skip")
            continue

        print(f"{symbol}: OK -> pass")
        screened.append(symbol)

    print("=== Screener Done ===")
    print(f"Passed: {screened}")

    return screened
