# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/paper_trader.py
# Назначение: Paper/live-цикл без Binance API
# Использует: strategy_selector, fetch_ohlcv, RiskManager
# ============================================

import logging
import time

from bot_ai.risk.manager import RiskManager
from bot_ai.strategy.strategy_selector import strategy_selector
from bot_ai.utils.data import fetch_ohlcv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

def run_trading_loop(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "volatile")

    StrategyClass = strategy_selector.get(strategy_name)
    if StrategyClass is None:
        logger.error(f"❌ Стратегия '{strategy_name}' не найдена.")
        return

    strategy = StrategyClass(cfg)
    risk = RiskManager(cfg)

    while True:
        df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            logger.warning("Нет данных с биржи. Повтор через 60 секунд.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        signal = strategy.generate_signal(df, cfg)
        if signal is None or signal["side"] == "flat":
            logger.info("Нет сигнала или flat.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        logger.info(f"Сигнал: {signal}")
        risk.execute(signal)

        time.sleep(cfg.get("poll_interval", 60))

def run_once(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "volatile")

    StrategyClass = strategy_selector.get(strategy_name)
    if StrategyClass is None:
        logger.error(f"❌ Стратегия '{strategy_name}' не найдена.")
        return

    strategy = StrategyClass(cfg)
    df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
    if df is None or df.empty:
        logger.warning("Нет данных с биржи.")
        return

    signal = strategy.generate_signal(df, cfg)
    if signal is None or signal["side"] == "flat":
        logger.info("Нет сигнала или flat.")
    else:
        logger.info(f"Сигнал: {signal}")
