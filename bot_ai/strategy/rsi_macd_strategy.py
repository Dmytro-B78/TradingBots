# ================================================================
# File: bot_ai/strategy/rsi_macd_strategy.py
# NT-Tech Hybrid RSI + MACD Strategy (optimized, MetaStrategy-compatible)
# O(1) per candle, no series recomputation
# ASCII-only, deterministic
# ================================================================

from bot_ai.strategy.base_strategy import BaseStrategy


class RSIMACDStrategy(BaseStrategy):
    """
    NT-Tech hybrid RSI + MACD strategy.
    BUY when RSI is oversold AND MACD crosses up.
    SELL when RSI is overbought AND MACD crosses down.
    """

    def __init__(self, params=None):
        super().__init__(params)

        self.rsi_period = int(self.params.get("rsi_period", 14))
        self.overbought = float(self.params.get("overbought", 70))
        self.oversold = float(self.params.get("oversold", 30))

        self.fast = int(self.params.get("fast", 12))
        self.slow = int(self.params.get("slow", 26))
        self.signal_period = int(self.params.get("signal", 9))

        self.prices = []
        self.regime = None

        self.avg_gain = None
        self.avg_loss = None

        self.fast_ema = None
        self.slow_ema = None
        self.macd = None
        self.signal_ema = None

        self.prev_macd = None
        self.prev_signal = None

        self.fast_k = 2.0 / (self.fast + 1.0)
        self.slow_k = 2.0 / (self.slow + 1.0)
        self.signal_k = 2.0 / (self.signal_period + 1.0)

    # ------------------------------------------------------------
    # Optional regime hook
    # ------------------------------------------------------------
    def set_regime(self, regime):
        self.regime = regime

    # ------------------------------------------------------------
    # Main candle handler (MetaStrategy-compatible)
    # ------------------------------------------------------------
    def on_candle(self, candle):
        price = candle["close"]
        self.prices.append(price)

        # --------------------------------------------------------
        # RSI (rolling)
        # --------------------------------------------------------
        if len(self.prices) >= 2:
            diff = self.prices[-1] - self.prices[-2]
            gain = diff if diff > 0 else 0.0
            loss = -diff if diff < 0 else 0.0

            if self.avg_gain is None:
                if len(self.prices) < self.rsi_period + 1:
                    return None
                gains = []
                losses = []
                for i in range(-self.rsi_period, 0):
                    d = self.prices[i] - self.prices[i - 1]
                    gains.append(d if d > 0 else 0.0)
                    losses.append(-d if d < 0 else 0.0)
                self.avg_gain = sum(gains) / float(self.rsi_period)
                self.avg_loss = sum(losses) / float(self.rsi_period)
            else:
                self.avg_gain = (self.avg_gain * (self.rsi_period - 1) + gain) / float(self.rsi_period)
                self.avg_loss = (self.avg_loss * (self.rsi_period - 1) + loss) / float(self.rsi_period)

            if self.avg_loss == 0.0:
                rsi = 100.0
            else:
                rs = self.avg_gain / self.avg_loss
                rsi = 100.0 - (100.0 / (1.0 + rs))
        else:
            return None

        # --------------------------------------------------------
        # MACD (incremental EMA)
        # --------------------------------------------------------
        if self.fast_ema is None:
            if len(self.prices) < self.slow:
                return None
            self.fast_ema = price
            self.slow_ema = price
            return None

        self.fast_ema = price * self.fast_k + self.fast_ema * (1.0 - self.fast_k)
        self.slow_ema = price * self.slow_k + self.slow_ema * (1.0 - self.slow_k)

        macd = self.fast_ema - self.slow_ema

        if self.signal_ema is None:
            self.signal_ema = macd
            self.prev_macd = macd
            self.prev_signal = self.signal_ema
            return None

        self.signal_ema = macd * self.signal_k + self.signal_ema * (1.0 - self.signal_k)

        macd_cross_up = self.prev_macd <= self.prev_signal and macd > self.signal_ema
        macd_cross_down = self.prev_macd >= self.prev_signal and macd < self.signal_ema

        self.prev_macd = macd
        self.prev_signal = self.signal_ema

        if rsi <= self.oversold and macd_cross_up:
            return "BUY"

        if rsi >= self.overbought and macd_cross_down:
            return "SELL"

        return None
