# ================================================================
# File: bot_ai/strategy/rsi_macd_strategy.py
# NT-Tech Hybrid RSI + MACD Strategy
# ASCII-only
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

    # ------------------------------------------------------------
    # RSI
    # ------------------------------------------------------------
    def compute_rsi(self):
        if len(self.prices) < self.rsi_period + 1:
            return None

        gains = []
        losses = []

        for i in range(-self.rsi_period, 0):
            diff = self.prices[i] - self.prices[i - 1]
            if diff >= 0:
                gains.append(diff)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(-diff)

        avg_gain = sum(gains) / self.rsi_period
        avg_loss = sum(losses) / self.rsi_period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))

    # ------------------------------------------------------------
    # EMA helper
    # ------------------------------------------------------------
    def ema(self, values, period):
        if len(values) < period:
            return None
        k = 2 / (period + 1)
        ema_val = sum(values[:period]) / period
        for v in values[period:]:
            ema_val = v * k + ema_val * (1 - k)
        return ema_val

    # ------------------------------------------------------------
    # MACD
    # ------------------------------------------------------------
    def compute_macd(self):
        if len(self.prices) < self.slow + self.signal_period:
            return None, None

        fast_ema = self.ema(self.prices, self.fast)
        slow_ema = self.ema(self.prices, self.slow)

        if fast_ema is None or slow_ema is None:
            return None, None

        macd = fast_ema - slow_ema

        macd_series = []
        for i in range(len(self.prices)):
            f = self.ema(self.prices[: i + 1], self.fast)
            s = self.ema(self.prices[: i + 1], self.slow)
            if f is not None and s is not None:
                macd_series.append(f - s)

        if len(macd_series) < self.signal_period:
            return macd, None

        signal = self.ema(macd_series, self.signal_period)
        return macd, signal

    # ------------------------------------------------------------
    # Combined signal
    # ------------------------------------------------------------
    def signal(self):
        rsi = self.compute_rsi()
        macd, signal = self.compute_macd()

        if rsi is None or macd is None or signal is None:
            return None

        prev_macd, prev_signal = self.compute_macd()
        if prev_macd is None or prev_signal is None:
            return None

        macd_cross_up = prev_macd <= prev_signal and macd > signal
        macd_cross_down = prev_macd >= prev_signal and macd < signal

        if rsi <= self.oversold and macd_cross_up:
            return "BUY"

        if rsi >= self.overbought and macd_cross_down:
            return "SELL"

        return None
