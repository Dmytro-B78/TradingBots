# bot_ai/live/bot_live.py
# Основной цикл запуска бота с использованием SignalExecutor

import logging
from bot_ai.signals.signal_generator import generate_signals
from bot_ai.execution.executor import SignalExecutor

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

executor = SignalExecutor()

def run(pairs, config):
    for pair in pairs:
        logger.info(f"Обработка пары: {pair}")
        try:
            signals = generate_signals(
                pair,
                timeframe=config.get("timeframe", "1h"),
                rsi_threshold=config.get("rsi_threshold", 70),
                strategy=config.get("strategy", "crossover")
            )
            if signals:
                for signal in signals:
                    logger.info(f"Сигнал: {signal}")
                    if not config.get("dry_run", True):
                        executor.execute_signal(pair, signal)
                    else:
                        logger.info("💡 Dry-run режим: ордер не отправлен.")
            else:
                logger.info("Сигналов нет.")
        except Exception as e:
            logger.error(f"Ошибка при обработке {pair}: {e}")
