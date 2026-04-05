# ================================================================
# File: bot_ai/strategy/meta_strategy.py
# NT-Tech MetaStrategy 2.6 (incremental filters, O(1) per candle)
# ASCII-only
# ================================================================

from bot_ai.strategy.ma_crossover_strategy import MACrossoverStrategy
from bot_ai.strategy.bollinger_strategy import BollingerStrategy
from bot_ai.strategy.macd_strategy import MACDStrategy
from bot_ai.strategy.rsi_strategy import RSIStrategy


class MetaStrategy:
    """
    NT-Tech MetaStrategy 2.6
    - incremental trend EMA
    - incremental ATR
    - trend slope filter
    - volatility ratio filter
    - ATR slope filter
    - O(1) per candle
    - orchestrates 4 sub-strategies
    """

    def __init__(self, params=None):
        self.params = params if isinstance(params, dict) else {}

        # Sub-strategies
        self.strategies = [
            MACrossoverStrategy(self.params.get("ma", {})),
            BollingerStrategy(self.params.get("boll", {})),
            MACDStrategy(self.params.get("macd", {})),
            RSIStrategy(self.params.get("rsi", {})),
        ]

        # Trend filter parameters
        self.trend_period = self.params.get("trend_period", 50)
        self.k_trend = 2 / (self.trend_period + 1)
        self.trend_ema = None
        self.prev_trend_ema = None
        self.min_slope = self.params.get("min_slope", 0.0)

        # ATR filter parameters
        self.atr_period = self.params.get("atr_period", 14)
        self.k_atr = 1 / self.atr_period
        self.atr = None
        self.prev_atr = None
        self.min_atr = self.params.get("min_atr", 0.1)
        self.min_volatility_ratio = self.params.get("min_volatility_ratio", 0.0005)

        # Previous candle for ATR
        self.prev_candle = None

    # ------------------------------------------------------------
    # Incremental trend filter
    # ------------------------------------------------------------
    def trend_ok(self, price):
        if self.trend_ema is None:
            self.trend_ema = price
            self.prev_trend_ema = price
            return False

        # Update EMA
        self.prev_trend_ema = self.trend_ema
        self.trend_ema = price * self.k_trend + self.trend_ema * (1 - self.k_trend)

        # Slope
        slope = self.trend_ema - self.prev_trend_ema

        # Conditions
        if price <= self.trend_ema:
            return False
        if slope <= self.min_slope:
            return False

        return True

    # ------------------------------------------------------------
    # Incremental ATR filter
    # ------------------------------------------------------------
    def atr_ok(self, candle):
        if self.prev_candle is None:
            self.prev_candle = candle
            return False

        high = candle.get("high")
        low = candle.get("low")
        close_prev = self.prev_candle.get("close")

        tr = max(
            high - low,
            abs(high - close_prev),
            abs(low - close_prev),
        )

        if self.atr is None:
            self.atr = tr
            self.prev_atr = tr
            self.prev_candle = candle
            return False

        # Update ATR
        self.prev_atr = self.atr
        self.atr = self.atr + self.k_atr * (tr - self.atr)

        self.prev_candle = candle

        # Conditions
        if self.atr < self.min_atr:
            return False

        # ATR must be rising
        if self.atr <= self.prev_atr:
            return False

        # Volatility ratio
        price = candle.get("close")
        if price is None:
            return False

        if (self.atr / price) < self.min_volatility_ratio:
            return False

        return True

    # ------------------------------------------------------------
    # Main orchestrator
    # ------------------------------------------------------------
    def on_candle(self, candle):
        price = candle.get("close")
        if price is None:
            return None

        # Filters
        if not self.trend_ok(price):
            return None

        if not self.atr_ok(candle):
            return None

        # Run sub-strategies
        for strat in self.strategies:
            s = strat.on_candle(candle)
            if s is None:
                continue

            # Normalize signals
            if s == "BUY":
                return {"signal": "OPEN_LONG"}

            if s == "SELL":
                return {"signal": "CLOSE_LONG"}

        return None
