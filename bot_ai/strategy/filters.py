# ================================================================
# File: bot_ai/strategy/filters.py
# NT-Tech 2026 - ATR-Regime 2.0 Filters (Adaptive)
# ASCII-only, deterministic, no Cyrillic
# ================================================================

class MetaFiltersResult:
    def __init__(self, passed, reason=None):
        self.passed = passed
        self.reason = reason


def apply_meta_filters(ctx):
    """
    ATR-Regime 2.0 entry filter (adaptive version).
    ctx = {
        "atr_1h_entry": float,
        "confidence_entry": float,
        "local_regime": str,
        "global_regime": str,
        "momentum": float (optional),
        "trend_strength": float (optional),
        "slope": float (optional),
    }
    """

    atr_regime = ctx.get("local_regime")
    conf = ctx.get("confidence_entry", 0.0)

    momentum = ctx.get("momentum", 0.0)
    trend_strength = ctx.get("trend_strength", 0.0)
    slope = ctx.get("slope", 0.0)

    # ------------------------------------------------------------
    # 1) Hard blocks (no entries allowed)
    # ------------------------------------------------------------
    if atr_regime in ["ultra_low", "extreme"]:
        return MetaFiltersResult(False, f"blocked_by_atr_regime_{atr_regime}")

    # ------------------------------------------------------------
    # 2) Low-volatility regime (weak market)
    # ------------------------------------------------------------
    if atr_regime == "low":
        if conf < 0.10:
            return MetaFiltersResult(False, "low_regime_conf_too_low")

    # ------------------------------------------------------------
    # 3) High-volatility regime (adaptive)
    # ------------------------------------------------------------
    if atr_regime == "high":
        # Allow entries with moderate confidence
        if conf < 0.02:
            return MetaFiltersResult(False, "high_regime_conf_too_low")

        # But require positive structure
        if momentum < 0:
            return MetaFiltersResult(False, "high_regime_negative_momentum")

        if trend_strength < 0:
            return MetaFiltersResult(False, "high_regime_negative_trend")

        if slope < 0:
            return MetaFiltersResult(False, "high_regime_negative_slope")

    # ------------------------------------------------------------
    # 4) Normal regime (best for entries)
    # ------------------------------------------------------------
    return MetaFiltersResult(True, None)
