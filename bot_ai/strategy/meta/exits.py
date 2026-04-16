# ================================================================
# File: bot_ai/strategy/meta/exits.py
# NT-Tech 2026 - Exits 3.0 (Dynamic RR, Soft-Exit Smoothing, ATR-Aware)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

def compute_dynamic_rr(trend_strength, slope, momentum, base_rr, atr_regime):
    """
    Computes dynamic RR for profit-lock based on trend structure and ATR regime.
    """

    trend_score = (
        0.5 * (trend_strength or 0.0) +
        0.3 * (slope or 0.0) +
        0.2 * (momentum or 0.0)
    )

    rr = base_rr

    if trend_score > 0.12:
        rr *= 1.15
    elif trend_score < 0.04:
        rr *= 0.90

    if atr_regime == "low":
        rr *= 0.90
    elif atr_regime == "high":
        rr *= 1.10
    elif atr_regime == "extreme":
        rr *= 0.80

    return max(1.1, min(rr, 2.2))


def smooth_soft_exit(prev_ema, raw_value, alpha):
    """
    EMA smoothing for soft-exit signal.
    """

    if raw_value < 0.0:
        raw_value = 0.0
    if raw_value > 1.0:
        raw_value = 1.0

    if prev_ema is None:
        return raw_value

    return alpha * raw_value + (1.0 - alpha) * prev_ema


def modulate_soft_exit_raw(raw_value, local_regime):
    """
    ATR-Regime 2.0 modulation of raw soft-exit signal.
    """

    if raw_value <= 0.0:
        return 0.0

    if local_regime == "low":
        raw_value *= 1.25
    elif local_regime == "high":
        raw_value *= 0.75
    elif local_regime == "extreme":
        raw_value *= 1.50

    if raw_value > 1.0:
        raw_value = 1.0

    return raw_value


def exit_profit_lock(strategy, close_price):
    """
    Existing profit-lock logic (called by MetaStrategy).
    This function is assumed to be already implemented in your codebase.
    Kept here as a placeholder to show that compute_dynamic_rr is used
    by MetaStrategy, not directly here.
    """
    # Implementation is in your current codebase.
    return None


def exit_soft(strategy,
              confidence,
              mtf_bias_4h,
              atr_regime_1h,
              momentum,
              trend_strength,
              local_regime):
    """
    Existing soft-exit decision function.
    This function returns a non-None value when soft-exit should trigger.
    Implementation is in your current codebase.
    """
    # Implementation is in your current codebase.
    return None
