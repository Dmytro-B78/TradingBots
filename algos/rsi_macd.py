# ================================================================
# File: algos/rsi_macd.py
# NT-Tech Algo: RSI + MACD Hybrid (lightweight)
# ASCII-only
# ================================================================

class RsiMacdAlgo:
    """
    Lightweight RSI + MACD algo.
    Used by StrategyRouter for fast hybrid signal generation.
    """

    def __init__(self, params=None):
        self.params = params or {}

        self.rsi_period = int(self.params.get("rsi_period", 14))
        self.overbought = float(self.params.get("overbought", 70))
        self.oversold = float(self.params.get("oversold", 30))

        self.fast = int(self.params.get("fast", 12))
        self.slow = int(self.params.get("slow", 26))
        self.signal_period = int(self.params.get("signal", 9))

        self.buffer = []

    # ------------------------------------------------------------
    # RSI
    # ------------------------------------------------------------
    def compute_rsi(self):
        if len(self.buffer) < self.rsi_period + 1:
            return None

        gains = []
        losses = []

        for i in range(-self.rsi_period, 0):
            diff = self.buffer[i] - self.buffer[i - 1]
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
    # EMA
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
        if len(self.buffer) < self.slow + self.signal_period:
            return None, None

        fast_ema = self.ema(self.buffer, self.fast)
        slow_ema = self.ema(self.buffer, self.slow)

        if fast_ema is None or slow_ema is None:
            return None, None

        macd = fast_ema - slow_ema

        macd_series = []
        for i in range(len(self.buffer)):
            f = self.ema(self.buffer[: i + 1], self.fast)
            s = self.ema(self.buffer[: i + 1], self.slow)
            if f is not None and s is not None:
                macd_series.append(f - s)

        if len(macd_series) < self.signal_period:
            return macd, None

        signal = self.ema(macd_series, self.signal_period)
        return macd, signal

    # ------------------------------------------------------------
    # Main execution
    # ------------------------------------------------------------
    def run(self, candles):
        signals = []

        for c in candles:
            price = c["close"]
            self.buffer.append(price)

            rsi = self.compute_rsi()
            macd, sig = self.compute_macd()

            if rsi is None or macd is None or sig is None:
                continue

            prev_macd, prev_sig = self.compute_macd()
            if prev_macd is None or prev_sig is None:
                continue

            macd_up = prev_macd <= prev_sig and macd > sig
            macd_down = prev_macd >= prev_sig and macd < sig

            if rsi <= self.oversold and macd_up:
                signals.append({"signal": "BUY", "price": price})

            if rsi >= self.overbought and macd_down:
                signals.append({"signal": "SELL", "price": price})

        return {
            "signals": signals,
            "params": self.params
        }
