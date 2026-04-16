# ================================================================
# File: bot_ai/strategy/meta/intrabar_stops.py
# NT-Tech 2026 - Intrabar Stops + ATR-Regime Modulation
# ASCII-only, deterministic, no Cyrillic
# ================================================================


# ------------------------------------------------------------
# ATR-Regime 2.0 trailing multiplier adjustment
# ------------------------------------------------------------
def adjust_trailing_mult_by_regime(base_mult, local_regime):
    mult = base_mult

    if local_regime == "low":
        mult = base_mult * 0.85
    elif local_regime == "normal":
        mult = base_mult * 1.00
    elif local_regime == "high":
        mult = base_mult * 1.15
    elif local_regime == "extreme":
        mult = base_mult * 1.30

    if mult < 0.6:
        mult = 0.6
    if mult > 2.0:
        mult = 2.0

    return mult


# ------------------------------------------------------------
# Absolute loss stop
# ------------------------------------------------------------
def intrabar_abs_stop(strategy, low_price):
    if strategy.entry_price is None:
        return None

    stop_price = strategy.entry_price * (1.0 + strategy.abs_loss_stop_pct)

    if low_price <= stop_price:
        return ("ABS_LOSS_STOP", stop_price)

    return None


# ------------------------------------------------------------
# High-watermark drawdown stop
# ------------------------------------------------------------
def intrabar_hwm_stop(strategy, low_price):
    if strategy.max_price_since_entry is None:
        return None

    stop_price = strategy.max_price_since_entry * (1.0 + strategy.hwm_drawdown_stop_pct)

    if low_price <= stop_price:
        return ("HWM_DRAWDOWN_STOP", stop_price)

    return None


# ------------------------------------------------------------
# ATR trailing stop
# ------------------------------------------------------------
def intrabar_atr_trail(strategy, low_price):
    if strategy.atr_1h is None or strategy.entry_price is None:
        return None

    stop_price = strategy.entry_price - strategy.atr_1h * strategy.atr_trail_mult

    if low_price <= stop_price:
        return ("ATR_TRAIL_STOP", stop_price)

    return None


# ------------------------------------------------------------
# EMA fast stop (softened)
# ------------------------------------------------------------
def intrabar_ema_stop(strategy, low_price):
    if strategy.ema_fast is None:
        return None

    # Softened EMA stop multiplier (was 1.0)
    stop_price = strategy.ema_fast * 0.985

    if low_price <= stop_price:
        return ("EMA_FAST_STOP", stop_price)

    return None
