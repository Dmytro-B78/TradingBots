# ============================================
# File: C:\TradingBots\NT\bot_ai\risk\manager.py
# Purpose: RiskManager — applies signal filtering
# Encoding: UTF-8
# ============================================

import pandas as pd

print("[risk_manager.py] Module loaded: RiskManager ready")

class RiskManager:
    def __init__(self, config):
        self.pair = config.get("pair", "BTCUSDT")
        self.qty = config.get("qty", 0.01)
        self.strategy = config.get("strategy", "unknown")
        self.interval = config.get("interval", "1h")

    def apply(self, signals, df):
        print("[RiskManager] apply() called")
        print("  type(signals):", type(signals))
        print("  type(df):", type(df))
        if hasattr(df, "columns"):
            print("  df.columns:", df.columns.tolist())
        else:
            print("  df has no columns")

        if not isinstance(signals, list):
            raise TypeError("signals must be a list")

        if not isinstance(df, pd.DataFrame):
            raise TypeError("df must be a pandas.DataFrame")

        trades = []

        for signal in signals:
            try:
                time = signal.get("time")
                direction = signal.get("direction")
                entry = signal.get("entry")

                if time is None or direction not in ("long", "short") or entry is None:
                    print(f"[SKIP] Invalid signal: {signal}")
                    continue

                row = df[df["time"] == time]
                if row.empty:
                    print(f"[SKIP] No row with time={time} in df")
                    continue

                price = row["close"].values[0]

                tp = entry * 1.01 if direction == "long" else entry * 0.99
                sl = entry * 0.995 if direction == "long" else entry * 1.005
                pnl = tp - entry if direction == "long" else entry - tp

                trades.append({
                    "time": time,
                    "pair": self.pair,
                    "strategy": self.strategy,
                    "interval": self.interval,
                    "direction": direction,
                    "entry": entry,
                    "tp": tp,
                    "sl": sl,
                    "pnl": pnl
                })

            except Exception as e:
                print(f"[ERROR] Failed to process signal {signal}: {e}")

        print(f"[RiskManager] Total trades after filtering: {len(trades)}")
        return trades
