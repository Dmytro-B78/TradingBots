import argparse
import json
import logging
import os

import pandas as pd

from strategies.breakout import BreakoutStrategy
from strategies.countertrend import CounterTrendStrategy
from strategies.mean_reversion import MeanReversionStrategy
from strategies.mock_data import generate_mock_data
from strategies.rsi import RSIStrategy
from strategies.sl_tp import SLTPStrategy
from strategies.sma import SMAStrategy

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/main.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("MAIN")

def load_config(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            cfg = json.load(f)
            logger.info(f"[MAIN] ? Загружен config: {path}")
            return cfg
    except Exception as e:
        logger.error(f"[MAIN] ? Ошибка загрузки config: {e}")
        return None

def load_best_config(csv_path):
    if not os.path.exists(csv_path):
        logger.error(f"[MAIN] ? Файл не найден: {csv_path}")
        return None
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            logger.error("[MAIN] ? opt_results.csv пуст")
            return None
        best = df.iloc[0].to_dict()
        logger.info(f"[MAIN] ? Загружены лучшие параметры: {best}")
        return best
    except Exception as e:
        logger.error(f"[MAIN] ? Ошибка чтения opt_results.csv: {e}")
        return None

def run_strategy(name, cfg, pair, force_optimize=False):
    strategy_map = {
        "mean_reversion": MeanReversionStrategy,
        "breakout": BreakoutStrategy,
        "sma": SMAStrategy,
        "rsi": RSIStrategy,
        "countertrend": CounterTrendStrategy,
        "sl_tp": SLTPStrategy
    }

    if name not in strategy_map:
        logger.error(f"[MAIN] ? Неизвестная стратегия: {name}")
        return

    if force_optimize:
        logger.info("[MAIN] ?? Запуск автооптимизации...")
        os.system("python optimize_parameters.py")
        cfg = load_best_config("results/opt_results.csv")
        if cfg is None:
            logger.error(
                "[MAIN] ? Не удалось загрузить параметры после оптимизации")
            return
        logger.info(
            "[MAIN] ? Запуск стратегии с оптимизированными параметрами")

    if cfg is None:
        logger.error("[MAIN] ? Конфигурация не загружена — прерывание")
        return

    logger.info(f"[MAIN] ? Стратегия: {name} | Пара: {pair}")
    try:
        strategy = strategy_map[name](cfg)
        df = generate_mock_data(pair, periods=200)

        if hasattr(strategy, "run"):
            trades = strategy.run(pair, df)
            logger.info(f"[MAIN] ? Сигналов: {len(trades)}")
            os.makedirs("results", exist_ok=True)
            pd.DataFrame(trades).to_csv(
                f"results/{name}_trades.csv", index=False)
        else:
            df = strategy.calculate_indicators(df)
            df = strategy.generate_signals(df)
            df = strategy.backtest(df)
            strategy.summary(pair)

        logger.info("[MAIN] ? Стратегия завершена успешно")
    except Exception as e:
        logger.exception(f"[MAIN] ? Ошибка выполнения стратегии: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pair", type=str, default="BTC/USDT")
    parser.add_argument("--strategy", type=str, default="mean_reversion")
    parser.add_argument("--config", type=str, default="config.json")
    parser.add_argument("--force-optimize", action="store_true")
    args = parser.parse_args()

    strat_name = args.strategy
    pair = args.pair

    if args.force_optimize:
        strat_cfg = None
    else:
        strat_cfg = load_config(args.config)

    run_strategy(
        strat_name,
        strat_cfg,
        pair,
        force_optimize=args.force_optimize)

