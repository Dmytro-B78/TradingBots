# ============================================
# File: C:\TradingBots\NT\bot_ai\utils\generate_report.py
# Purpose: Generate trade performance report from trades_log.csv
# Encoding: UTF-8
# ============================================

import pandas as pd
from pathlib import Path

LOG_PATH = Path("trades_log.csv")
REPORT_PATH = Path("trades_report.txt")

def generate_report():
    if not LOG_PATH.exists():
        print("❌ trades_log.csv not found.")
        return

    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("⚠️ trades_log.csv is empty.")
        return

    total_trades = len(df)
    total_pnl = df["pnl"].sum()
    avg_pnl = df["pnl"].mean()
    win_trades = df[df["pnl"] > 0]
    loss_trades = df[df["pnl"] < 0]
    win_rate = len(win_trades) / total_trades * 100

    summary = f"""
📊 TRADE REPORT
===========================
Total trades     : {total_trades}
Winning trades   : {len(win_trades)}
Losing trades    : {len(loss_trades)}
Win rate         : {win_rate:.2f}%
Total PnL        : {total_pnl:.2f}
Average PnL      : {avg_pnl:.2f}
===========================
"""

    print(summary)
    REPORT_PATH.write_text(summary.strip(), encoding="utf-8")
    print(f"✅ Report saved to {REPORT_PATH.resolve()}")

if __name__ == "__main__":
    generate_report()
