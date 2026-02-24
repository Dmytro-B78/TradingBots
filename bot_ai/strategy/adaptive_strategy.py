# ============================================
# File: bot_ai/strategy/adaptive_strategy.py
# Purpose: Adaptive strategy with ATR, ADX, and higher timeframe trend filters
# Format: UTF-8 without BOM
# Compatible with: Signal, config, logging
# ============================================

import pandas as pd
import logging
from bot_ai.filters.entry_filters import atr_filter, adx_filter
from bot_ai.indicators import calculate_atr, calculate_adx, calculate_sma
from bot_ai.data_loader import load_data
from bot_ai.core.signal import Signal

def higher_tf_trend_ok(higher_df: pd.DataFrame, lookback: int = 20) -> bool:
    if len(higher_df) < lookback:
        logging.debug(f"[FILTER:mtf] Not enough candles for higher timeframe trend (required={lookback}, actual={len(higher_df)})")
        return False
    sma = calculate_sma(higher_df["close"], period=lookback)
    close = higher_df["close"].iloc[-1]
    ma = sma.iloc[-1]
    passed = close > ma
    logging.debug(f"[FILTER:mtf] close={close:.8f} > SMA({lookback})={ma:.8f} → passed={passed}")
    return passed

def adaptive_strategy(pair: str, df: pd.DataFrame, config: dict) -> list:
    signals = []

    if df is None or df.empty or len(df) < 50:
        logging.debug(f"[SKIP] {pair} | insufficient candles (len={len(df)})")
        return signals

    df = df.copy()

    # === ATR filter ===
    if not atr_filter(df, config):
        logging.debug(f"[FILTER:atr] {pair} | rejected by ATR filter")
        return signals
    logging.debug(f"[FILTER:atr] {pair} | passed")

    # === ADX filter ===
    if not adx_filter(df, config):
        logging.debug(f"[FILTER:adx] {pair} | rejected by ADX filter")
        return signals
    logging.debug(f"[FILTER:adx] {pair} | passed")

    # === Higher timeframe trend filter ===
    if config.get("enable_mtf_filter", False):
        higher_tf = config.get("higher_tf", "4h")
        higher_df = load_data(pair, higher_tf, limit=100)
        if not higher_tf_trend_ok(higher_df):
            logging.debug(f"[FILTER:mtf] {pair} | higher timeframe trend not confirmed")
            return signals
        logging.debug(f"[FILTER:mtf] {pair} | higher timeframe trend confirmed")

    # === Signal generation ===
    close = df["close"].iloc[-1]
    stop_loss_pct = config.get("stop_loss_pct", 0.02)
    rr = config.get("min_risk_reward_ratio", 1.5)

    entry = round(close, 8)
    stop = round(entry * (1 - stop_loss_pct), 8)
    target = round(entry * (1 + stop_loss_pct * rr), 8)

    signal = Signal(
        action="buy",
        symbol=pair,
        time=df.index[-1],
        entry_price=entry,
        stop_loss=stop,
        target_price=target,
        strategy_name="adaptive"
    )
    logging.info(f"[SIGNAL] {signal}")
    signals.append(signal)

    return signals
