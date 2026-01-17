# sma.py
# Назначение: Стратегия на основе пересечения скользящих средних
# Структура:
# └── bot_ai/strategy/sma.py

class SMAStrategy:
    def __init__(self, cfg):
        self.cfg = cfg

    def run(self, symbol, df):
        df = df.copy()
        df["sma_fast"] = df["close"].rolling(self.cfg["sma_fast"]).mean()
        df["sma_slow"] = df["close"].rolling(self.cfg["sma_slow"]).mean()

        df["signal"] = 0
        df.loc[df["sma_fast"] > df["sma_slow"], "signal"] = 1
        df.loc[df["sma_fast"] < df["sma_slow"], "signal"] = -1

        trades = []
        for i in range(1, len(df)):
            if df["signal"].iloc[i] == 1 and df["signal"].iloc[i - 1] != 1:
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
