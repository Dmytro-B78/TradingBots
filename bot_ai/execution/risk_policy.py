# ================================================================
# File: bot_ai/execution/risk_policy.py
# NT-Tech Risk Policy 1.0
# - Pure functions for risk, stops, sizing
# ASCII-only, deterministic
# ================================================================

def compute_confidence_scale(confidence):
    if confidence is None:
        return 1.0, 1.0

    c = max(min(confidence, 1.0), -1.0)
    c_abs = abs(c)

    risk_scale = 0.5 + c_abs * 0.8
    size_scale = 0.7 + c_abs * 0.6

    return risk_scale, size_scale


def compute_risk_pct(
    base_risk_pct,
    max_risk_pct,
    min_risk_pct,
    atr_1h,
    atr_4h,
    atr_regime_1h,
    atr_regime_4h,
    local_regime,
    global_regime,
    mtf_bias_4h,
    confidence,
    atr_ratio_shock,
    shock_risk_scale,
    trend_risk_boost,
    range_risk_scale,
    compression_risk_scale,
    expansion_risk_scale,
):
    atr_ratio = None
    if atr_4h is not None and atr_4h > 0:
        atr_ratio = atr_1h / atr_4h

    shock = False
    if atr_ratio is not None and atr_ratio >= atr_ratio_shock:
        shock = True
    if atr_regime_1h == "extreme" or atr_regime_4h == "extreme":
        shock = True

    risk_pct = base_risk_pct

    if local_regime == "trend":
        risk_pct *= trend_risk_boost
    elif local_regime == "range":
        risk_pct *= range_risk_scale
    elif local_regime == "compression":
        risk_pct *= compression_risk_scale
    elif local_regime == "expansion":
        risk_pct *= expansion_risk_scale

    if global_regime == "trend":
        risk_pct *= 1.05
    elif global_regime == "compression":
        risk_pct *= 0.85

    if mtf_bias_4h is not None:
        if mtf_bias_4h >= 0.6:
            risk_pct *= 1.10
        elif mtf_bias_4h <= 0.2:
            risk_pct *= 0.85

    if atr_regime_1h == "low":
        risk_pct *= 0.9
    elif atr_regime_1h == "high":
        risk_pct *= 0.9
    elif atr_regime_1h == "extreme":
        risk_pct *= 0.5

    if shock:
        risk_pct *= shock_risk_scale

    risk_scale, _ = compute_confidence_scale(confidence)
    risk_pct *= risk_scale

    risk_pct = max(min(risk_pct, max_risk_pct), min_risk_pct)

    return risk_pct, atr_ratio


def compute_stop_mult(
    stop_mult_base,
    stop_mult_low_vol,
    stop_mult_high_vol,
    stop_mult_extreme_vol,
    atr_regime_1h,
    atr_regime_4h,
    global_regime,
    mtf_bias_4h,
    atr_ratio,
    confidence,
):
    if atr_regime_1h == "low":
        stop_mult = stop_mult_low_vol
    elif atr_regime_1h == "high":
        stop_mult = stop_mult_high_vol
    elif atr_regime_1h == "extreme":
        stop_mult = stop_mult_extreme_vol
    else:
        stop_mult = stop_mult_base

    if atr_regime_4h == "high":
        stop_mult *= 1.10
    elif atr_regime_4h == "extreme":
        stop_mult *= 1.25

    if global_regime == "trend":
        stop_mult *= 1.10
    elif global_regime == "compression":
        stop_mult *= 0.90

    if mtf_bias_4h is not None:
        if mtf_bias_4h >= 0.6:
            stop_mult *= 1.15
        elif mtf_bias_4h <= 0.2:
            stop_mult *= 0.90

    if atr_ratio is not None and atr_ratio > 1.8:
        stop_mult *= 1.20

    if confidence is not None:
        c_abs = abs(max(min(confidence, 1.0), -1.0))
        stop_mult *= (1.0 + c_abs * 0.4)

    return stop_mult


def compute_sizing_factors(price, atr_1h, local_regime, confidence):
    atr_factor = 1.0
    if atr_1h is not None and atr_1h > 0 and price > 0:
        atr_norm = min(max(atr_1h / price, 0.0001), 0.02)
        atr_factor = 1.0 / (1.0 + atr_norm * 25.0)

    _, conf_scale = compute_confidence_scale(confidence)

    regime_factor = 1.0
    if local_regime == "trend":
        regime_factor = 1.15
    elif local_regime == "range":
        regime_factor = 0.85
    elif local_regime == "compression":
        regime_factor = 0.75

    return atr_factor, conf_scale, regime_factor
