# ================================================================
# File: bot_ai/config/config.py
# Module: config.config
# Purpose: Central NT-Tech configuration
# Responsibilities:
#   - Define default strategy
#   - Define backtest parameters
#   - Define paths
# Notes:
#   - ASCII-only
# ================================================================

import os

class Config:
    """
    NT-Tech global configuration.
    """

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

    BACKTEST_DATA_DIR = r"C:\TradingBots\candles\compiled"

    BACKTEST_DEFAULT_SYMBOL = "SOLUSDT"
    BACKTEST_DEFAULT_INTERVAL = "1m"

    INITIAL_BALANCE = 10000.0

    DEFAULT_STRATEGY = "ma_crossover"

    DEFAULT_PARAMS = {
        "short_period": 10,
        "long_period": 30
    }
