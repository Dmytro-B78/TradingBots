# ============================================
# File: bot_ai/utils/portfolio_report.py
# Purpose: Accurate FIFO-based portfolio report with commission-aware investment tracking
# Supports: --env main | test
# Requires: pip install python-binance python-dotenv
# ============================================

import os
import argparse
from decimal import Decimal
from datetime import datetime
from binance.client import Client
from dotenv import load_dotenv

load_dotenv()

def get_api_keys(env):
    if env == "test":
        return os.getenv("BINANCE_TESTNET_API_KEY"), os.getenv("BINANCE_TESTNET_API_SECRET")
    else:
        return os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_API_SECRET")

def get_current_price(client, symbol):
    try:
        ticker = client.get_symbol_ticker(symbol=symbol)
        return Decimal(ticker["price"])
    except:
        return None

def format_time(ms):
    return datetime.utcfromtimestamp(ms / 1000).strftime("%Y-%m-%d %H:%M")

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
    balances = {b["asset"]: Decimal(b["free"]) + Decimal(b["locked"]) for b in account["balances"]}

    print(f"\n📦 Portfolio Snapshot ({args.env.upper()}):\n")

    total_portfolio_cost = Decimal("0")

    for asset, qty in balances.items():
        if asset == "USDT" or qty == 0:
            continue

        symbol = asset + "USDT"
        try:
            trades = client.get_my_trades(symbol=symbol)
        except:
            continue

        trades.sort(key=lambda x: x["time"])
        fifo_queue = []
        for t in trades:
            t_qty = Decimal(t["qty"])
            t_price = Decimal(t["price"])
            t_time = format_time(t["time"])
            t_id = t["id"]
            commission = Decimal(t["commission"])
            commission_asset = t["commissionAsset"]

            if t["isBuyer"]:
                net_qty = t_qty
                if commission_asset == asset:
                    net_qty -= commission
                fifo_queue.append({"qty": net_qty, "price": t_price, "time": t_time, "id": t_id})
            else:
                sell_qty = t_qty
                if commission_asset == asset:
                    sell_qty += commission
                while sell_qty > 0 and fifo_queue:
                    lot = fifo_queue[0]
                    if lot["qty"] <= sell_qty:
                        sell_qty -= lot["qty"]
                        fifo_queue.pop(0)
                    else:
                        lot["qty"] -= sell_qty
                        sell_qty = Decimal("0")

        if not fifo_queue:
            continue

        total_cost = sum(lot["qty"] * lot["price"] for lot in fifo_queue)
        total_qty = sum(lot["qty"] for lot in fifo_queue)
        avg_price = (total_cost / total_qty).quantize(Decimal("0.0001"))
        current_price = get_current_price(client, symbol)
        if current_price is None:
            continue
        pnl_pct = ((current_price - avg_price) / avg_price * 100).quantize(Decimal("0.01"))

        print(f"{symbol} | Balance: {total_qty:.6f} | Avg Buy: {avg_price:.4f} | Now: {current_price:.4f} | PnL: {pnl_pct:+.2f}%")
        print("  FIFO breakdown:")
        for lot in fifo_queue:
            print(f"    {lot['qty']:.6f} @ {lot['price']:.4f} | {lot['time']} | ID: {lot['id']}")
        print(f"  ➤ Invested in {symbol}: {total_cost:.2f} USDT\n")

        total_portfolio_cost += total_cost

    print(f"💰 Total invested (FIFO-based, net of commissions): {total_portfolio_cost:.2f} USDT")

if __name__ == "__main__":
    main()
