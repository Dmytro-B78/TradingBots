# -*- coding: utf-8 -*-
# ============================================
# File: C:\TradingBots\NT\main.py
# Purpose: Live trading with RSI strategy and symbol filtering
# Format: UTF-8 without BOM
# ============================================

import argparse
import json
import os
import time
import pandas as pd
from datetime import datetime, timezone
from binance.client import Client
from dotenv import load_dotenv
from bot_ai.strategy.breakout import BreakoutStrategy
from bot_ai.strategy.mean_reversion import MeanReversionStrategy
from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
from bot_ai.core.order_manager import OrderManager
from bot_ai.metrics import calculate_metrics

load_dotenv()

def load_config(path):
    with open(path, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def fetch_latest_candles(client, symbol, interval, limit=100):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    df = pd.DataFrame(klines, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["time"] = pd.to_datetime(df["close_time"], unit="ms")
    df["close"] = df["close"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    return df[["time", "close", "high", "low"]]

def get_seconds_until_next_candle(interval):
    now = datetime.now(timezone.utc)
    seconds = {"1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800, "1h": 3600, "4h": 14400, "1d": 86400}.get(interval, 60)
    elapsed = (now.minute * 60 + now.second) % seconds
    return seconds - elapsed + 2

def log_csv(path, row):
    os.makedirs("logs", exist_ok=True)
    df = pd.DataFrame([row])
    if not os.path.exists(path):
        df.to_csv(path, index=False)
    else:
        df.to_csv(path, mode="a", header=False, index=False)

def filter_symbols(client, config):
    tickers = client.get_ticker()
    volume_threshold = config["risk"]["min_24h_volume_usdt"]
    max_spread = config["risk"]["max_spread_pct"] / 100
    min_volatility = config["risk"]["min_volatility"]
    top_n = config["risk"]["top_n_pairs"]

    filtered = []
    for t in tickers:
        if not t["symbol"].endswith("USDT"):
            continue
        try:
            vol = float(t["quoteVolume"])
            ask = float(t["askPrice"])
            bid = float(t["bidPrice"])
            spread = (ask - bid) / ask if ask > 0 else 1
            high = float(t["highPrice"])
            low = float(t["lowPrice"])
            volatility = (high - low) / low if low > 0 else 0
            if vol >= volume_threshold and spread <= max_spread and volatility >= min_volatility:
                filtered.append((t["symbol"], vol))
        except:
            continue

    filtered.sort(key=lambda x: x[1], reverse=True)
    return [s[0] for s in filtered[:top_n]]

def run_live(strategy, symbol, timeframe, client, initial_balance=1000, fee_rate=0.001):
    print(f"⚡ Live trading started for {symbol} | Timeframe: {timeframe}")
    balance, position, min_notional = initial_balance, 0.0, 5
    while True:
        try:
            df = fetch_latest_candles(client, symbol, interval=timeframe, limit=100)
            signal = strategy.generate_signal(df)
            price = float(df["close"].iloc[-1])
            now = datetime.now(timezone.utc)

            if signal:
                log_csv(f"logs/{symbol}_signals.csv", {
                    "timestamp": now.isoformat(), "symbol": signal.symbol,
                    "action": signal.action, "price": signal.price
                })
                print(f"[{now}] SIGNAL: {signal.action.upper()} @ {price:.4f}")

                if signal.action == "buy" and balance >= min_notional and position == 0:
                    qty = balance / price
                    if qty * price >= min_notional:
                        fee = qty * fee_rate
                        position = qty - fee
                        balance = 0
                        log_csv(f"logs/{symbol}_orders.csv", {
                            "timestamp": now.isoformat(), "symbol": symbol,
                            "action": "buy", "price": price,
                            "balance": round(balance, 2), "fee": round(fee, 4)
                        })
                        print(f"[{now}] BUY executed @ {price:.4f} | Fee: {fee:.4f}")
                elif signal.action == "sell" and position > 0:
                    proceeds = position * price
                    if proceeds >= min_notional:
                        fee = proceeds * fee_rate
                        balance = proceeds - fee
                        position = 0
                        log_csv(f"logs/{symbol}_orders.csv", {
                            "timestamp": now.isoformat(), "symbol": symbol,
                            "action": "sell", "price": price,
                            "balance": round(balance, 2), "fee": round(fee, 4)
                        })
                        print(f"[{now}] SELL executed @ {price:.4f} | Fee: {fee:.4f}")
            else:
                print(f"[{now}] No signal.")

            log_csv(f"logs/{symbol}_balance.csv", {
                "timestamp": now.isoformat(),
                "balance_cash": round(balance, 2),
                "position_qty": round(position, 6),
                "price": round(price, 4),
                "total_value": round(balance + position * price, 2)
            })

            print(f"[{now}] STATUS | Balance: {balance:.2f} | Position: {position:.6f} | Value: {balance + position * price:.2f}")

        except Exception as e:
            print(f"❌ Error in live loop: {e}")
        time.sleep(get_seconds_until_next_candle(timeframe))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["backtest", "live"], required=True)
    parser.add_argument("--symbol")
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--balance", type=float, default=1000)
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    print(f"🚀 Mode: {args.mode} | Strategy: {args.strategy} | Timeframe: {args.timeframe}")
    config = load_config(args.config)
    params = config.get("params", {})
    params["symbol"] = args.symbol

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    client = Client(api_key, api_secret)

    if args.mode == "live" and not args.symbol:
        symbols = filter_symbols(client, config)
        print(f"✅ Filtered symbols: {symbols}")
        return

    if not args.symbol:
        print("❌ Symbol is required for backtest/live mode.")
        return

    order_manager = OrderManager(client=client, test_mode=(args.mode != "live"))
    if args.strategy == "breakout":
        strategy = BreakoutStrategy({"params": params})
    elif args.strategy == "mean_reversion":
        strategy = MeanReversionStrategy(params)
    elif args.strategy == "rsi":
        strategy = RSIReversalStrategy(params)
    else:
        print(f"❌ Unknown strategy: {args.strategy}")
        return

    if args.mode == "backtest":
        df_path = f"data/{args.symbol}_{args.timeframe}.csv"
        if not os.path.exists(df_path):
            print(f"❌ Data not found: {df_path}")
            return
        df = pd.read_csv(df_path)
        df["time"] = pd.to_datetime(df["time"])
        df = strategy.calculate_indicators(df)
        df = strategy.generate_signals(df)
        strategy.backtest(df, initial_balance=args.balance)
        summary_df = strategy.summary(args.symbol)
        if summary_df.empty:
            print("❌ No trades found.")
            return
        metrics = calculate_metrics(summary_df, initial_balance=args.balance)
        for k, v in metrics.items():
            print(f"{k:>20}: {v}")
    elif args.mode == "live":
        run_live(strategy, args.symbol, args.timeframe, client, initial_balance=args.balance)

if __name__ == "__main__":
    main()
