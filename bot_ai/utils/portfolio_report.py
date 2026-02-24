# ============================================
# File: bot_ai/utils/portfolio_report.py
# Purpose: Portfolio snapshot with FIFO-based buy breakdown and PnL
# Supports: --env main | test
# Requires: pip install python-binance python-dotenv
# ============================================

import os
import argparse
from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Select API keys
def get_api_keys(env):
    if env == "test":
        return os.getenv("BINANCE_TESTNET_API_KEY"), os.getenv("BINANCE_TESTNET_API_SECRET")
    else:
        return os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET")

# Get current market price
def get_current_price(client, symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return Decimal(ticker["price"])
    except:
        return None

# Main logic
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", choices=["main", "test"], default="main", help="Environment: main or test")
    args = parser.parse_args()

    api_key, api_secret = get_api_keys(args.env)
    if not api_key or not api_secret:
        print(f"❌ Missing API keys for environment: {args.env}")
        return

    client = Client(api_key, api_secret)
    if args.env == "test":
        client.API_URL = "https://testnet.binance.vision/api"

    account = client.get_account()
    balances = [b for b in account["balances"] if float(b["free"]) > 0 or float(b["locked"]) > 0]

    print(f"\n📦 Portfolio Snapshot ({args.env.upper()}):\n")

    for b in balances:
        asset = b["asset"]
        qty = Decimal(b["free"]) + Decimal(b["locked"])
        if asset == "USDT" or qty == 0:
            continue

        symbol = asset + "USDT"
        try:
            trades = client.get_my_trades(symbol=symbol)
        except:
            continue

        # Sort trades by time (FIFO)
        buy_trades = [t for t in trades if t["isBuyer"]]
        buy_trades.sort(key=lambda x: x["time"])

        remaining_qty = qty
        fifo_lots = []
        total_cost = Decimal("0")
        total_qty = Decimal("0")

        for t in buy_trades:
            price = Decimal(t["price"])
            t_qty = Decimal(t["qty"])
            if remaining_qty <= 0:
                break
            used_qty = min(remaining_qty, t_qty)
            fifo_lots.append((used_qty, price))
            total_cost += used_qty * price
            total_qty += used_qty
            remaining_qty -= used_qty

        if total_qty == 0:
            continue

        avg_price = (total_cost / total_qty).quantize(Decimal("0.0001"))
        current_price = get_current_price(client, symbol)
        if current_price is None:
            continue

        pnl_pct = ((current_price - avg_price) / avg_price * 100).quantize(Decimal("0.01"))

        print(f"{asset} | Total: {qty:.6f} | Avg Buy: {avg_price:.4f} | Now: {current_price:.4f} | PnL: {pnl_pct:+.2f}%")
        print("  Breakdown (remaining lots only):")
        for amount, price in fifo_lots:
            print(f"    {amount:.6f} @ {price:.4f}")
        print("")

if __name__ == "__main__":
    main()
