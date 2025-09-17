import logging
from bot_ai.core.config import load_config
from bot_ai.core.logging_setup import setup_logging
from bot_ai.selector.pipeline import fetch_and_filter_pairs
from bot_ai.strategy.simple_ma import run_strategy

def main():
    cfg = load_config()
    logger = setup_logging(cfg.logging.level, cfg.logging.file)

    logger.info(f"Запуск {cfg.bot_name} ({cfg.bot_short})")
    logger.info(f"Режим работы: {cfg.mode}")
    logger.info(f"Биржа: {cfg.exchange}")

    pairs = fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24)
    logger.info(f"Whitelist: {pairs}")

    # Запуск стратегии
    run_strategy(cfg, pairs)

if __name__ == '__main__':
    main()
