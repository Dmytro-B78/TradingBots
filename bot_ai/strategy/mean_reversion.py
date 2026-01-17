# ============================================
# 📈 mean_reversion.py — стратегия SMA + RSI
# --------------------------------------------
# Обновление: сохраняем timestamp в self.trades
# ============================================

import pandas as pd
import logging

logger = logging.getLogger(__name__)

class MeanReversionStrategy:
    def __init__(self, config):
        self.config = config
        self.trades = []

    def calculate_indicators(self, df):
        df["sma_fast"] = df["close"].rolling(self.config["sma_fast"]).mean()
        df["sma_slow"] = df["close"].rolling(self.config["sma_slow"]).mean()
        df["rsi"] = self._rsi(df["close"], self.config["rsi_period"])
        return df

    def generate_signals(self, df):
        df["signal"] = 0
        df.loc[
            (df["sma_fast"] > df["sma_slow"]) & (df["rsi"] < 30),
            "signal"
        ] = 1
        df.loc[
            (df["sma_fast"] < df["sma_slow"]) & (df["rsi"] > 70),
            "signal"
        ] = -1
        return df

    def backtest(self, df):
        if "timestamp" not in df.columns:
            logger.warning("[BACKTEST] timestamp отсутствует — добавим NaT")
            df["timestamp"] = pd.NaT

        df["position"] = df["signal"].shift()
        df["returns"] = df["close"].pct_change()
        df["strategy"] = df["position"] * df["returns"]
        df["pnl"] = df["strategy"].fillna(0)

        # Сохраняем timestamp в trades
        self.trades = df[df["position"].notnull()][["timestamp", "pnl"]].copy()

    def summary(self, symbol):
        if isinstance(self.trades, pd.DataFrame):
            df = self.trades.copy()
            if "timestamp" not in df.columns:
                logger.error("[SUMMARY] Отсутствуют колонки: ['timestamp']")
                df["timestamp"] = pd.NaT
            df["symbol"] = symbol
            return df[["timestamp", "symbol", "pnl"]]
        else:
            logger.warning("[SUMMARY] trades не определены")
            return pd.DataFrame(columns=["timestamp", "symbol", "pnl"])

    def _rsi(self, series, period):
        delta = series.diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
