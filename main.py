# ============================================
# File: main.py
# Purpose: CLI-совместимость с test_cli_entrypoint_runs
# ============================================

import time
import logging
from bot_ai.selector.pipeline import select_pairs
from bot_ai.exec.executor import TradeExecutor

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def main():
    logger.info("[MAIN] Запуск основного скрипта")
    executor = TradeExecutor()
    pairs = select_pairs(None)
    logger.info(f"[MAIN] Пары: {pairs}")
    while True:
        time.sleep(1)

# При импорте модуля сразу запускаем main()
main()
