# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/paper_trader.py
# Purpose: Paper/live trading loop without Binance API
# Uses: StrategySelector, fetch_ohlcv, RiskManager
# Format: UTF-8 without BOM
# ============================================

import logging
import time
from bot_ai.risk.manager import RiskManager
from bot_ai.strategy.strategy_selector import StrategySelector
from bot_ai.utils.data import fetch_ohlcv
from bot_ai.core.signal import Signal

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

# === Continuous trading loop ===
def run_trading_loop(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "volatile")

    selector = StrategySelector(config={"strategies": [strategy_name]})
    risk = RiskManager(cfg)

    while True:
        df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            logger.warning("No OHLCV data. Retrying in 60 seconds.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        context = {"df": df, "symbol": pair, "time": time.time()}
        signal = selector.select(context)

        if not isinstance(signal, Signal) or signal.side == "flat":
            logger.info("No actionable signal.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        logger.info(f"Signal: {signal}")
        risk.execute(signal)

        time.sleep(cfg.get("poll_interval", 60))

# === One-time signal evaluation ===
def run_once(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "volatile")

    selector = StrategySelector(config={"strategies": [strategy_name]})
    df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
    if df is None or df.empty:
        logger.warning("No OHLCV data.")
        return

    context = {"df": df, "symbol": pair, "time": time.time()}
    signal = selector.select(context)

    if not isinstance(signal, Signal) or signal.side == "flat":
        logger.info("No signal or flat.")
    else:
        logger.info(f"Signal: {signal}")
