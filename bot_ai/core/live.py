import os
import time
import pandas as pd
from datetime import datetime, timezone
from pathlib import Path
from bot_ai.metrics import calculate_metrics

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
    seconds = {
        "1m": 60, "3m": 180, "5m": 300, "15m": 900, "30m": 1800,
        "1h": 3600, "2h": 7200, "4h": 14400, "6h": 21600,
        "8h": 28800, "12h": 43200, "1d": 86400, "3d": 259200,
        "1w": 604800, "1M": 2592000
    }.get(interval, 60)
    elapsed = (now.minute * 60 + now.second) % seconds
    return seconds - elapsed + 2

def log_csv(path, row):
    df_row = pd.DataFrame([row])
    if not os.path.exists(path):
        df_row.to_csv(path, index=False)
    else:
        df_row.to_csv(path, mode="a", header=False, index=False)

def run_live(strategy, symbol, timeframe, client, initial_balance=1000, fee_rate=0.001, paper_mode=False):
    print(f"⚡ {'Paper' if paper_mode else 'Live'} trading started for {symbol} | Timeframe: {timeframe}")
    balance, position, min_notional = initial_balance, 0.0, 5
    price = None
    try:
        while True:
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
                        print(f"[{now}] {'PAPER' if paper_mode else 'REAL'} BUY @ {price:.4f} | Fee: {fee:.4f}")
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
            time.sleep(get_seconds_until_next_candle(timeframe))

    except KeyboardInterrupt:
        print("\nSession interrupted. Generating summary...")

    if paper_mode:
        print("\n=== PAPER TRADING SUMMARY ===")
        try:
            df_balance = pd.read_csv(f"logs/{symbol}_balance.csv")
            final_value = df_balance["total_value"].iloc[-1]
        except Exception:
            final_value = balance + position * price if price else balance

        try:
            df_orders = pd.read_csv(f"logs/{symbol}_orders.csv")
            total_trades = len(df_orders)
        except Exception:
            total_trades = 0

        win_rate = "N/A"
        print(f"Total Trades: {total_trades}")
        print(f"Final Balance: {final_value:.2f}")
        print(f"Win Rate: {win_rate}")

        metrics = pd.DataFrame([{
            "symbol": symbol,
            "total_trades": total_trades,
            "final_balance": final_value,
            "win_rate": win_rate
        }])
        os.makedirs("logs", exist_ok=True)
        metrics.to_csv("logs/top10.csv", mode="a", header=not os.path.exists("logs/top10.csv"), index=False)
