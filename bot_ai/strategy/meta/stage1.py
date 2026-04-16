# ================================================================
# File: bot_ai/strategy/meta/stage1.py
# NT-Tech 2026 - Stage 1 (Base Entry Conditions)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

def stage1_check(strategy, confidence, local_regime):
    """
    Stage 1: base entry conditions.
    Checks minimal trend, slope, momentum and confidence thresholds.
    """

    # Confidence threshold
    if confidence < strategy.s1_min_conf:
        return False

    # Trend strength
    if strategy.trend_strength < strategy.s1_min_trend:
        return False

    # Slope
    if strategy.slope < strategy.s1_min_slope:
        return False

    # Momentum
    if strategy.momentum < strategy.s1_min_momentum:
        return False

    return True
