# bot_ai/cli_entrypoint.py
# CLI-запуск бота с загрузкой конфигурации пользователя

import argparse
import logging
import yaml

from bot_ai.utils.logger import setup_logger
from bot_ai.live.bot_live import run as run_bot

setup_logger('bot')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def load_config(path="config.yaml"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Ошибка загрузки конфигурации: {e}")
        return {}

def run(argv=None):
    parser = argparse.ArgumentParser(description="Запуск торгового бота")
    parser.add_argument("--config", type=str, default="config.yaml", help="Путь к YAML-файлу конфигурации")
    args = parser.parse_args(argv)

    config = load_config(args.config)
    if not config:
        logger.error("Конфигурация не загружена. Завершение.")
        return

    pairs = config.get("pairs", ["BTCUSDT"])
    logger.info(f"Запуск бота. Пары: {pairs}, стратегия: {config.get('strategy')}")

    run_bot(pairs, config)

def main(argv=None):
    run(argv)

if __name__ == "__main__":
    main()
