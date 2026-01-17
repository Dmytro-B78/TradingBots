# bot_ai/utils/logger.py
# Настройка логирования в файл и консоль

import logging
import os
from datetime import datetime

def setup_logger(name="bot"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
