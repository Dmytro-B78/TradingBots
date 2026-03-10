# ============================================
# File: C:\TradingBots\NT\bot_ai\selector\pipeline_select_pairs.py
# Purpose: Select USDT pairs (test-friendly)
# Encoding: UTF-8 without BOM
# ============================================

import logging
import ccxt
from bot_ai.strategy.strategy_loader import load_strategy
from . import pipeline_utils


def cfg_get(cfg, key, default=None):
    if isinstance(cfg, dict):
        return cfg.get(key, default)
    return getattr(cfg, key, default)


def detect_regime(*args, **kwargs):
    return "neutral"


def get_exchange_client(cfg):
    exchange_cfg = cfg_get(cfg, "exchange", {})
    api_key = cfg_get(exchange_cfg, "apiKey")
    secret = cfg_get(exchange_cfg, "secret")
    testnet = cfg_get(exchange_cfg, "testnet", False)

    params = {"apiKey": api_key, "secret": secret}

    if testnet:
        params["options"] = {"defaultType": "spot"}
        params["urls"] = {"api": {"public": "https://testnet.binance.vision/api"}}

    return ccxt.binance(params)


def select_pairs(cfg, risk_guard=None):
    logging.info("[SELECTOR] >>> START select_pairs()")

    client = get_exchange_client(cfg)

    logging.info("[SELECTOR] Loading exchange info...")

    # --- MODE 1: ccxt client ---
    if hasattr(client, "load_markets"):
        markets = client.load_markets()
        symbols = list(markets.keys())

        def get_ticker(sym):
            return client.fetch_ticker(sym)

    # --- MODE 2: MockClient from tests ---
    elif hasattr(client, "exchange_info"):
        info = client.exchange_info()
        symbols = [s["symbol"] for s in info["symbols"]]

        # Build ticker map
        tickers = {t["symbol"]: t for t in client.ticker_24hr()}

        def get_ticker(sym):
            return tickers.get(sym)

    else:
        raise RuntimeError("Unsupported exchange mock")

    raw_pairs = []

    for s in symbols:
        raw_symbol = s
        ccxt_symbol = s if "/" in s else s.replace("USDT", "/USDT")

        # Try raw symbol first (mock), then ccxt symbol
        ticker = get_ticker(raw_symbol) or get_ticker(ccxt_symbol)
        if not ticker:
            continue

        try:
            volume = float(ticker.get("quoteVolume", 0))
            price = float(ticker.get("lastPrice", ticker.get("last", 0)))
            ask = float(ticker.get("askPrice", ticker.get("ask", 0)))
            bid = float(ticker.get("bidPrice", ticker.get("bid", 0)))
        except Exception:
            continue

        if ask == 0 or bid == 0:
            continue

        spread = (ask - bid) / ask * 100

        raw_pairs.append({
            "pair": raw_symbol,
            "volume": volume,
            "price": price,
            "spread": spread
        })

    risk_cfg = cfg_get(cfg, "risk", {})
    top_n = cfg_get(risk_cfg, "top_n_pairs", 20)
    top_pairs = raw_pairs[:top_n]

    # Strategy selection (optional)
    strategy_cfg = cfg_get(cfg, "strategy", None)

    if strategy_cfg:
        strategy_name = cfg_get(strategy_cfg, "name")
        strategy_params = cfg_get(strategy_cfg, "params", {})

        StrategyClass = load_strategy(strategy_name)

        for pair in top_pairs:
            symbol = pair["pair"]
            params = dict(strategy_params)
            params["symbol"] = symbol

            strategy = StrategyClass(params)

            df = pipeline_utils.get_data(
                symbol=symbol,
                interval="1h",
                lookback=50,
                source="binance",
                testnet=cfg_get(cfg_get(cfg, "exchange", {}), "testnet", False)
            )

            signal = strategy.generate_signal(df)
            if signal:
                pipeline_utils.log_signal(signal)

    logging.info("[SELECTOR] <<< END select_pairs()")
    return top_pairs
