import pandas as pd
import logging
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal
from bot_ai.core.context import MarketContext

class RsiStrategy(BaseStrategy):
    def __init__(self, config):
        super().__init__(config)
        params = config.get("strategy_params", {}).get("rsi", {})
        self.period = params.get("rsi_period", 14)
        self.rsi_buy = params.get("rsi_oversold", 30)
        self.rsi_sell = params.get("rsi_overbought", 70)

    def generate_signal(self, context):
        df = context.df.copy()
        if len(df) < self.period + 1:
            return None

        delta = df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(self.period).mean()
        avg_loss = loss.rolling(self.period).mean()

        rs = avg_gain / (avg_loss + 1e-6)
        df["rsi"] = 100 - (100 / (1 + rs))
        rsi = df["rsi"].iloc[-1]

        if pd.isna(rsi):
            return None
        elif rsi < self.rsi_buy:
            return Signal("buy", context.symbol, context.time, rsi=rsi)
        elif rsi > self.rsi_sell:
            return Signal("sell", context.symbol, context.time, rsi=rsi)
        else:
            return None

    def run(self, symbol, cfg):
        client = self.get_exchange_client(cfg)
        timeframe = cfg.get("timeframe", "1h")
        limit = cfg.get("lookback_candles", 100)

        ohlcv = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv or len(ohlcv) < self.period + 1:
            logging.warning(f"[RSI] Недостаточно данных для {symbol}")
            return

        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
        context = MarketContext(symbol, timeframe, df)
        signal = self.generate_signal(context)

        if signal:
            logging.info(f"[RSI] Сигнал по {symbol}: {signal}")
        else:
            logging.debug(f"[RSI] Нет сигнала по {symbol}")
