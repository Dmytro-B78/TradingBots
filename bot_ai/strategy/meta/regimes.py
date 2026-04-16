# ================================================================
# File: bot_ai/strategy/meta/regimes.py
# NT-Tech 2026 - ATR-Regime 2.0 (Institutional Volatility Classifier)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

def classify_atr_regime(atr_norm):
    """
    ATR-Regime 2.0 classification based on normalized ATR.
    atr_norm = atr_1h / atr_1h_mean
    """

    if atr_norm is None or atr_norm <= 0:
        return "unknown"

    if atr_norm < 0.65:
        return "ultra_low"

    if atr_norm < 0.85:
        return "low"

    if atr_norm < 1.25:
        return "normal"

    if atr_norm < 1.75:
        return "high"

    return "extreme"


def update_regimes(strategy):
    """
    Updates:
    - atr_norm_1h
    - atr_norm_4h
    - atr_regime_1h
    - atr_regime_4h
    - local_regime
    - global_regime
    """

    atr_1h = strategy.atr_1h
    atr_4h = strategy.atr_4h
    atr_1h_mean = strategy.atr_1h_mean
    atr_4h_mean = strategy.atr_4h_mean

    # ------------------------------------------------------------
    # ATR normalization
    # ------------------------------------------------------------
    if atr_1h and atr_1h_mean and atr_1h_mean > 0:
        atr_norm_1h = atr_1h / atr_1h_mean
    else:
        atr_norm_1h = None

    if atr_4h and atr_4h_mean and atr_4h_mean > 0:
        atr_norm_4h = atr_4h / atr_4h_mean
    else:
        atr_norm_4h = None

    strategy.atr_norm_1h = atr_norm_1h
    strategy.atr_norm_4h = atr_norm_4h

    # ------------------------------------------------------------
    # ATR regimes
    # ------------------------------------------------------------
    strategy.atr_regime_1h = classify_atr_regime(atr_norm_1h)
    strategy.atr_regime_4h = classify_atr_regime(atr_norm_4h)

    # ------------------------------------------------------------
    # Local regime (fast)
    # ------------------------------------------------------------
    # Local regime is based on 1h ATR regime
    strategy.local_regime = strategy.atr_regime_1h

    # ------------------------------------------------------------
    # Global regime (slow)
    # ------------------------------------------------------------
    # Global regime is based on 4h ATR regime
    strategy.global_regime = strategy.atr_regime_4h

    # ------------------------------------------------------------
    # Multi-timeframe bias (already computed in indicators)
    # ------------------------------------------------------------
    # strategy.mtf_bias_4h is updated in indicators.py
    return strategy
