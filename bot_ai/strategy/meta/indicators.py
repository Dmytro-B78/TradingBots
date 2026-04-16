# ================================================================
# File: bot_ai/strategy/meta/indicators.py
# NT-Tech 2026 - EMA, ATR, Momentum, Slope, Trend, MTF Bias
# ASCII-only, deterministic, no Cyrillic
# ================================================================

def ema(prev, value, alpha):
    if prev is None:
        return value
    return alpha * value + (1.0 - alpha) * prev


def true_range(prev_close, high, low):
    if prev_close is None:
        return abs(high - low)
    return max(high - low, abs(high - prev_close), abs(low - prev_close))


def update_indicators(strategy, candle):
    # ------------------------------------------------------------
    # Bar index
    # ------------------------------------------------------------
    strategy.bar_index += 1

    # ------------------------------------------------------------
    # Extract OHLC
    # ------------------------------------------------------------
    close = float(candle["close"])
    high = float(candle["high"])
    low = float(candle["low"])
    open_price = float(candle.get("open", close))

    strategy.prev_close = strategy.last_close
    strategy.prev_open = strategy.last_open
    strategy.prev_high = strategy.last_high
    strategy.prev_low = strategy.last_low

    strategy.last_close = close
    strategy.last_open = open_price
    strategy.last_high = high
    strategy.last_low = low

    # ------------------------------------------------------------
    # EMA calculations
    # ------------------------------------------------------------
    alpha_fast = 2.0 / max(strategy.ema_fast_len, 2)
    alpha_slow = 2.0 / max(strategy.ema_slow_len, 2)
    alpha_trend = 2.0 / max(strategy.ema_trend_len, 2)

    strategy.prev_ema_fast = strategy.ema_fast
    strategy.ema_fast = ema(strategy.ema_fast, close, alpha_fast)
    strategy.ema_slow = ema(strategy.ema_slow, close, alpha_slow)
    strategy.ema_trend = ema(strategy.ema_trend, close, alpha_trend)

    # ------------------------------------------------------------
    # ATR calculations
    # ------------------------------------------------------------
    tr = true_range(strategy.prev_close, high, low)
    strategy.atr_1h = ema(strategy.atr_1h, tr, strategy.atr_1h_alpha)
    strategy.atr_4h = ema(strategy.atr_4h, tr, strategy.atr_4h_alpha)

    if strategy.atr_1h is not None:
        strategy.atr_1h_mean = ema(strategy.atr_1h_mean, strategy.atr_1h, 0.01)
    if strategy.atr_4h is not None:
        strategy.atr_4h_mean = ema(strategy.atr_4h_mean, strategy.atr_4h, 0.01)

    # ------------------------------------------------------------
    # Trend strength
    # ------------------------------------------------------------
    if strategy.ema_fast and strategy.ema_slow and strategy.atr_1h and strategy.atr_1h > 0:
        ts_raw = (strategy.ema_fast - strategy.ema_slow) / (strategy.atr_1h * 0.5)
        strategy.trend_strength = max(min(ts_raw, 4.0), -4.0) / 4.0
    else:
        strategy.trend_strength = 0.0

    # ------------------------------------------------------------
    # Slope
    # ------------------------------------------------------------
    if strategy.ema_fast and strategy.prev_ema_fast and strategy.atr_1h and strategy.atr_1h > 0:
        slope_raw = (strategy.ema_fast - strategy.prev_ema_fast) / (strategy.atr_1h * 0.25)
        strategy.slope = max(min(slope_raw, 4.0), -4.0) / 4.0
    else:
        strategy.slope = 0.0

    # ------------------------------------------------------------
    # Momentum
    # ------------------------------------------------------------
    if strategy.prev_close and strategy.atr_1h and strategy.atr_1h > 0:
        mom_raw = (close - strategy.prev_close) / (strategy.atr_1h * 0.25)
        strategy.momentum = max(min(mom_raw, 4.0), -4.0) / 4.0
    else:
        strategy.momentum = 0.0

    # ------------------------------------------------------------
    # Push histories
    # ------------------------------------------------------------
    _push_hist(strategy.momentum_hist, strategy.momentum)
    _push_hist(strategy.slope_hist, strategy.slope)
    _push_hist(strategy.trend_hist, strategy.trend_strength)

    # ------------------------------------------------------------
    # Update max price since entry
    # ------------------------------------------------------------
    if strategy.position == "LONG":
        if strategy.max_price_since_entry is None:
            strategy.max_price_since_entry = close
        else:
            if close > strategy.max_price_since_entry:
                strategy.max_price_since_entry = close

    # ------------------------------------------------------------
    # NEW: Multi-timeframe bias (4h)
    # ------------------------------------------------------------
    # Simple, robust bias:
    # +1 if ema_fast > ema_trend
    # -1 if ema_fast < ema_trend
    # 0 if equal or undefined
    # Then smooth with EMA to avoid noise.
    # ------------------------------------------------------------
    raw_bias = 0.0
    if strategy.ema_fast is not None and strategy.ema_trend is not None:
        if strategy.ema_fast > strategy.ema_trend:
            raw_bias = 1.0
        elif strategy.ema_fast < strategy.ema_trend:
            raw_bias = -1.0

    # Smooth bias
    if strategy.mtf_bias_4h == 0.0:
        strategy.mtf_bias_4h = raw_bias
    else:
        strategy.mtf_bias_4h = ema(strategy.mtf_bias_4h, raw_bias, 0.10)


def _push_hist(buf, value, max_len=5):
    buf.append(value)
    if len(buf) > max_len:
        del buf[0]
