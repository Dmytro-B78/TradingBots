# bot_ai/core/logger.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def get_logger(name: str, log_dir: str = "logs",
               level: str = "INFO") -> logging.Logger:
    lvl = getattr(logging, level.upper(), logging.INFO)
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(lvl)
    if logger.handlers:
        return logger
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    file_handler = RotatingFileHandler(
        Path(log_dir) / f"{name}.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=5)
    file_handler.setFormatter(fmt)
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    logger.addHandler(file_handler)
    logger.addHandler(console)
    logger.propagate = False
    return logger

