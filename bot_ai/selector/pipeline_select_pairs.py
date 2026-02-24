# ============================================
# File: bot_ai/selector/pipeline_select_pairs.py
# Purpose: Select all available USDT pairs from Binance Spot Testnet (no filters)
# Encoding: UTF-8
# ============================================

import logging
import json
import os
import csv
import time
from binance.spot import Spot

def get_exchange_client(cfg):
    if cfg["exchange"].get("testnet", False):
        base_url = "https://testnet.binance.vision"
    else:
        base_url = "https://api.binance.com"

    return Spot(
        api_key=cfg["exchange"].get("apiKey"),
        api_secret=cfg["exchange"].get("secret"),
        base_url=base_url
    )

def select_pairs(cfg):
    t0 = time.time()
    logging.info("[SELECTOR] >>> START select_pairs()")

    client = get_exchange_client(cfg)

    t1 = time.time()
    logging.info("[SELECTOR] Loading exchange info...")
    info = client.exchange_info()
    symbols = [s for s in info["symbols"] if s["quoteAsset"] == "USDT" and s["status"] == "TRADING"]
    logging.info(f"[SELECTOR] Loaded {len(symbols)} USDT pairs in {time.time() - t1:.2f}s")

    raw_pairs = []
    t2 = time.time()

    tickers = {t["symbol"]: t for t in client.ticker_24hr()}
    for s in symbols:
        symbol = s["symbol"]
        ticker = tickers.get(symbol)
        if not ticker:
            continue

        try:
            volume = float(ticker.get("quoteVolume", 0))
            price = float(ticker.get("lastPrice", 0))
            ask = float(ticker.get("askPrice", 0))
            bid = float(ticker.get("bidPrice", 0))
        except Exception:
            continue

        if ask == 0 or bid == 0:
            continue

        spread = (ask - bid) / ask * 100
        raw_pairs.append({
            "symbol": symbol,
            "volume": volume,
            "price": price,
            "spread": spread
        })

    logging.info(f"[SELECTOR] {len(raw_pairs)} pairs collected (in {time.time() - t2:.2f}s)")
    for p in raw_pairs:
        logging.info(f"[PAIR] {p['symbol']} | Volume: {p['volume']:.0f} | Price: {p['price']} | Spread: {p['spread']:.2f}%")

    top_n = cfg["risk"].get("top_n_pairs", 20)
    top_pairs = raw_pairs[:top_n]
    selected_symbols = [p["symbol"] for p in top_pairs]

    logging.info(f"[SELECTED] Top {top_n} pairs (no filters):")
    for p in top_pairs:
        logging.info(f"  {p['symbol']} | Volume: {p['volume']:.0f} | Spread: {p['spread']:.2f}%")

    os.makedirs("data", exist_ok=True)

    with open("data/whitelist.json", "w", encoding="utf-8") as f:
        json.dump(selected_symbols, f, indent=2)
    logging.info(f"[SAVE] Saved {len(selected_symbols)} pairs to data/whitelist.json")

    metrics_path = "data/pair_metrics.csv"
    with open(metrics_path, "w", newline="", encoding="utf-8") as csvfile:
        import csv
        writer = csv.DictWriter(csvfile, fieldnames=["symbol", "volume", "price", "spread"])
        writer.writeheader()
        for row in raw_pairs:
            writer.writerow(row)
    logging.info(f"[SAVE] Saved metrics for {len(raw_pairs)} pairs to {metrics_path}")

    logging.info(f"[SELECTOR] <<< END select_pairs() in {time.time() - t0:.2f}s")
    return top_pairs
