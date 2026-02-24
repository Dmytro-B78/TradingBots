import pandas as pd
import logging
from bot_ai.strategy.base_strategy import BaseStrategy
from bot_ai.core.signal import Signal
from bot_ai.core.context import MarketContext

class SMAStrategy(BaseStrategy):
    def __init__(self, config):
        super().__init__(config)
        params = config.get("strategy_params", {}).get("sma", {})
        self.fast = params.get("sma_fast", 5)
        self.slow = params.get("sma_slow", 10)

    def generate_signal(self, context):
        df = context.df.copy()
        if len(df) < self.slow + 2:
            return None

        df["sma_fast"] = df["close"].rolling(self.fast).mean()
        df["sma_slow"] = df["close"].rolling(self.slow).mean()

        prev_fast = df["sma_fast"].iloc[-2]
        prev_slow = df["sma_slow"].iloc[-2]
        curr_fast = df["sma_fast"].iloc[-1]
        curr_slow = df["sma_slow"].iloc[-1]

        if pd.isna(prev_fast) or pd.isna(prev_slow) or pd.isna(curr_fast) or pd.isna(curr_slow):
            return None

        if prev_fast < prev_slow and curr_fast > curr_slow:
            return Signal("buy", context.symbol, context.time, crossover="bullish")
        elif prev_fast > prev_slow and curr_fast < curr_slow:
            return Signal("sell", context.symbol, context.time, crossover="bearish")
        else:
            return None

    def run(self, symbol, cfg):
        client = self.get_exchange_client(cfg)
        timeframe = cfg.get("timeframe", "1h")
        limit = cfg.get("lookback_candles", 100)

        ohlcv = client.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        if not ohlcv or len(ohlcv) < self.slow + 2:
            logging.warning(f"[SMA] Недостаточно данных для {symbol}")
            return

        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
        context = MarketContext(symbol, timeframe, df)
        signal = self.generate_signal(context)

        if signal:
            logging.info(f"[SMA] Сигнал по {symbol}: {signal}")
        else:
            logging.debug(f"[SMA] Нет сигнала по {symbol}")
