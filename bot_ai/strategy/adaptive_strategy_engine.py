# ============================================
# File: bot_ai/strategy/adaptive_strategy_engine.py
# Purpose: Adaptive engine for selecting strategy and generating signals
# Format: UTF-8 without BOM
# Compatible with: strategy catalog, Signal, logging
# ============================================

import pandas as pd
import logging
from bot_ai.strategy.strategy_router import classify_market_conditions, match_strategy
from bot_ai.strategy.strategy_catalog import STRATEGY_CATALOG
from bot_ai.strategy.strategy_loader import load_strategy_class
from bot_ai.core.signal import Signal

def analyze_and_select(pair: str, df: pd.DataFrame, config: dict) -> dict | None:
    if df is None or df.empty or len(df) < 50:
        logging.debug(f"[ENGINE] {pair} | insufficient candles (len={len(df)})")
        return None

    df = df.copy()

    # === Market condition classification ===
    from bot_ai.strategy.mean_reversion import MeanReversionStrategy
    df = MeanReversionStrategy({}).calculate_indicators(df)
    market = classify_market_conditions(df)
    logging.debug(f"[ENGINE] {pair} | market condition classified as '{market}'")

    # === Strategy selection ===
    strategy_name = match_strategy(market)
    if not strategy_name:
        logging.debug(f"[ENGINE] {pair} | no strategy matched for market='{market}'")
        return None
    logging.debug(f"[ENGINE] {pair} | selected strategy: {strategy_name}")

    # === Load strategy and parameters ===
    strategy_class = load_strategy_class(strategy_name)
    params = STRATEGY_CATALOG[strategy_name].get("default_params", {})
    strategy = strategy_class({"params": params})

    # === Signal generation ===
    signal = strategy.generate_signal(df)
    if not signal:
        logging.debug(f"[ENGINE] {pair} | strategy '{strategy_name}' returned no signal")
        return None

    if isinstance(signal, Signal):
        logging.info(f"[ENGINE] {pair} | signal generated: {signal}")
        return {
            "symbol": pair,
            "strategy": strategy_name,
            "signal": signal,
            "params": params
        }

    logging.warning(f"[ENGINE] {pair} | unexpected signal format from strategy '{strategy_name}'")
    return None
