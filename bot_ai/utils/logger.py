# ============================================
# File: C:\TradingBots\NT\bot_ai\utils\logger.py
# Purpose: Signal logger for strategies and live trading
# Format: UTF-8 without BOM
# ============================================

import logging
import os

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(LOG_DIR, "signals.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def log_signal(message):
    print(message)
    logging.info(message)
