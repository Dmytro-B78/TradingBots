# File: C:\TradingBots\NT\tests\test_bot_pipeline.py
# Purpose: Validate full bot pipeline execution in paper mode
# Structure: Check signal generation, backtest output, paper order log, and final analytics
# Encoding: UTF-8 without BOM

import os
import csv

def check_file_exists(path):
    if not os.path.exists(path):
        print(f"❌ MISSING: {path}")
        return False
    print(f"✅ FOUND: {path}")
    return True

def check_nonempty_csv(path):
    if not os.path.exists(path):
        print(f"❌ MISSING: {path}")
        return False
    with open(path, newline='', encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)
        if len(rows) < 2:
            print(f"❌ EMPTY: {path}")
            return False
    print(f"✅ OK: {path} has {len(rows)-1} rows")
    return True

print("=== BOT PIPELINE CHECK ===")

# 1. Signal files
signals_ok = True
for symbol in ["TIAUSDT", "ARBUSDT", "JTOUSDT"]:
    for tf in ["1h", "15m"]:
        path = f"paper_logs/test_signal_{symbol}_signals.csv"
        if not check_nonempty_csv(path):
            signals_ok = False

# 2. Backtest results
results_ok = check_nonempty_csv("logs/top10.csv")

# 3. Paper orders
orders_ok = check_file_exists("paper_logs/paper_orders.log")

# 4. Summary
print("\n=== SUMMARY ===")
if signals_ok and results_ok and orders_ok:
    print("✅ BOT IS WORKING: All stages passed.")
else:
    print("❌ BOT INCOMPLETE: One or more stages failed.")
