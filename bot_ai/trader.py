# === bot_ai/trader.py ===
# Торговый цикл с поддержкой стратегии "adaptive"

import logging
import time

from bot_ai.risk.manager import RiskManager
from bot_ai.strategy import strategy_selector
from bot_ai.utils.data import fetch_ohlcv

logger = logging.getLogger(__name__)

def run_trading_loop(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "adaptive")

    strategy = strategy_selector.get(strategy_name)
    if strategy is None:
        logger.error(f"Стратегия '{strategy_name}' не найдена.")
        return

    risk = RiskManager(cfg)

    while True:
        df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            logger.warning("Нет данных для анализа.")
            time.sleep(60)
            continue

        signal = strategy.generate_signal(df, cfg)
        if signal is None:
            logger.info("Нет сигнала.")
            time.sleep(60)
            continue

        if signal["side"] == "flat":
            logger.info("Сигнал: flat — пропускаем.")
            time.sleep(60)
            continue

        logger.info(f"Сигнал: {signal}")
        risk.execute(signal)

        time.sleep(cfg.get("poll_interval", 60))

