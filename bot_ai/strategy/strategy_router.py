# ============================================
# Path: C:\TradingBots\NT\bot_ai\strategy\strategy_router.py
# Purpose: Automatic strategy selection based on market conditions
# Updated: Compatible with strategy catalog and routing logic
# Format: UTF-8 without BOM, production-ready
# ============================================

import logging
from bot_ai.strategy.strategy_catalog import STRATEGY_CATALOG
from bot_ai.strategy.strategy_loader import load_strategy_class

logger = logging.getLogger(__name__)

def classify_market_conditions(df):
    """
    Analyze market and return condition dictionary:
    {volatility, trend, rsi, volume}
    """
    recent = df.tail(50).copy()
    volatility = recent["close"].pct_change().std()
    trend = recent["close"].iloc[-1] - recent["close"].iloc[0]
    avg_volume = recent["volume"].mean()

    trend_strength = "up" if trend > 0 else "down" if trend < 0 else "flat"
    vol_level = "high" if volatility > 0.05 else "medium" if volatility > 0.02 else "low"

    return {
        "volatility": volatility,
        "volatility_level": vol_level,
        "trend": trend_strength,
        "rsi": recent["rsi"].iloc[-1] if "rsi" in recent.columns else None,
        "volume": avg_volume
    }

def match_strategy(market_conditions):
    """
    Select strategy from catalog that matches current market conditions.
    """
    for name, meta in STRATEGY_CATALOG.items():
        cond = meta.get("conditions", {})
        match = True

        for key, rule in cond.items():
            val = market_conditions.get(key)
            if val is None:
                match = False
                break
            if isinstance(rule, str):
                try:
                    if rule.startswith("<") and not val < float(rule[1:]):
                        match = False
                    elif rule.startswith(">") and not val > float(rule[1:]):
                        match = False
                    elif rule in ["up", "down", "flat", "strong", "any"] and val != rule:
                        match = False
                    elif "or" in rule:
                        options = [r.strip() for r in rule.split("or")]
                        if not any(str(val).startswith(opt) or str(val) == opt for opt in options):
                            match = False
                except Exception:
                    match = False

        if match:
            logger.info(f"[ROUTER] Strategy selected: {name}")
            return name

    logger.warning("[ROUTER] No matching strategy found.")
    return None

def route_strategy(df, config):
    """
    Entry point: selects and initializes strategy based on market.
    """
    df = df.copy()
    from bot_ai.strategy.mean_reversion import MeanReversionStrategy
    df = MeanReversionStrategy({}).calculate_indicators(df)

    market = classify_market_conditions(df)
    strategy_name = match_strategy(market)

    if strategy_name:
        strategy_class = load_strategy_class(strategy_name)
        params = STRATEGY_CATALOG[strategy_name].get("default_params", {})
        return strategy_class({"params": params})
    else:
        raise RuntimeError("No suitable strategy could be determined.")
