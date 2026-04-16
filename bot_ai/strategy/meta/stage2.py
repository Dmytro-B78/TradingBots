# ================================================================
# File: bot_ai/strategy/meta/stage2.py
# NT-Tech 2026 - Stage 2 (Signal Quality Filter)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

def stage2_check(strategy, confidence, local_regime):
    """
    Stage 2: quality filter.
    Ensures the signal is strong enough to justify an entry.
    """

    # Confidence threshold
    if confidence < strategy.s2_min_conf:
        return False

    # Trend strength
    if strategy.trend_strength < strategy.s2_min_trend:
        return False

    # Slope
    if strategy.slope < strategy.s2_min_slope:
        return False

    # Momentum
    if strategy.momentum < strategy.s2_min_momentum:
        return False

    # Multi-timeframe bias (4h)
    if strategy.mtf_bias_4h < strategy.s2_min_mtf_bias_4h:
        return False

    return True
