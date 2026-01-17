# rsi.py
# Назначение: Стратегия на основе индикатора RSI
# Структура:
# └── bot_ai/strategy/rsi.py

import pandas as pd

class RSIStrategy:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, symbol, df):
        df = df.copy()
        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(self.cfg["rsi_period"]).mean()
        avg_loss = loss.rolling(self.cfg["rsi_period"]).mean()
        rs = avg_gain / (avg_loss + 1e-9)
        df["rsi"] = 100 - (100 / (1 + rs))

        trades = []
        for i in range(1, len(df)):
            if df["rsi"].iloc[i] < self.cfg["rsi_buy"]:
                entry = df["close"].iloc[i]
                stop = entry * (1 - self.cfg["stop_loss_pct"])
                target = entry * (1 + self.cfg["min_risk_reward_ratio"] * self.cfg["stop_loss_pct"])
                trades.append({
                    "entry": entry,
                    "stop": stop,
                    "target": target,
                    "side": "long"
                })

        metrics = {
            "total_return": 0,
            "final_value": 0,
            "num_trades": len(trades),
            "win_rate": 0,
            "avg_trade_return": 0,
            "sharpe_ratio": 0,
            "max_drawdown": 0
        }

        return metrics, trades
