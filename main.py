import logging
import time
import os
from datetime import datetime

import ccxt
import pandas as pd

from bot_ai.core.config import load_config
from bot_ai.backtest.backtest_engine import run_backtest
from bot_ai.strategy.sma_for_backtest import sma_strategy
from bot_ai.strategy.rsi_for_backtest import rsi_strategy
from bot_ai.selector.pipeline import select_pairs
from bot_ai.exec.executor import TradeExecutor
from bot_ai.risk.guard import RiskGuard
from bot_ai.utils.notifier import Notifier  # ← добавили

# === Инициализация ===
cfg = load_config("config.json")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# === Инициализация RiskGuard и Notifier ===
risk_guard = RiskGuard(cfg)
notifier = Notifier(cfg)  # ← создаём экземпляр уведомителя

# === Отбор пар ===
logging.info("Запуск отбора пар через селектор...")
pairs = select_pairs(cfg, risk_guard=risk_guard)

if not pairs:
    logging.warning("Селектор не вернул ни одной пары.")
else:
    logging.info(f"Отобрано {len(pairs)} пар: {pairs}")

    # === Backtest ===
    if getattr(cfg, "enable_backtest", False):
        logging.info("=== Запуск backtest для SMA ===")
        run_backtest(cfg, pairs, sma_strategy, "SMA", days=30, timeframes=["1h", "4h", "1d"])
        logging.info("=== Запуск backtest для RSI ===")
        run_backtest(cfg, pairs, rsi_strategy, "RSI", days=30, timeframes=["1h", "4h", "1d"])
        logging.info("=== Все тесты завершены ===")

    # === Live / Dry-run ===
    if getattr(cfg, "mode", "dry-run") in ["live", "dry-run"]:
        mode = cfg.mode
        logging.info(f"=== Запуск торгового режима: {mode} ===")

        executor = TradeExecutor(cfg, risk_guard=risk_guard, notifier=notifier)  # ← передаём notifier
        exchange = getattr(ccxt, cfg.exchange)({'enableRateLimit': True})

        trade_loop_interval = getattr(cfg, "trade_loop_interval_sec", 60)
        ohlcv_limit = getattr(cfg, "live_ohlcv_limit", 100)
        timeframe = getattr(cfg, "live_timeframe", "1h")

        strategies = [
            (sma_strategy, "SMA"),
            (rsi_strategy, "RSI"),
        ]

        while True:
            logging.info("=== Новый цикл торговли ===")

            # --- Проверка SL/TP для открытых позиций ---
            for symbol, pos in list(executor.positions.items()):
                try:
                    last_price = exchange.fetch_ticker(symbol)["last"]

                    # LONG
                    if pos["side"] == "buy":
                        if pos["sl"] and last_price <= pos["sl"]:
                            logging.info(f"SL сработал для {symbol} (LONG) @ {last_price}")
                            executor.execute_trade(symbol, "sell", last_price, None)
                        elif pos["tp"] and last_price >= pos["tp"]:
                            logging.info(f"TP сработал для {symbol} (LONG) @ {last_price}")
                            executor.execute_trade(symbol, "sell", last_price, None)

                    # SHORT
                    elif pos["side"] == "sell":
                        if pos["sl"] and last_price >= pos["sl"]:
                            logging.info(f"SL сработал для {symbol} (SHORT) @ {last_price}")
                            executor.execute_trade(symbol, "buy", last_price, None)
                        elif pos["tp"] and last_price <= pos["tp"]:
                            logging.info(f"TP сработал для {symbol} (SHORT) @ {last_price}")
                            executor.execute_trade(symbol, "buy", last_price, None)

                except Exception as e:
                    logging.error(f"Ошибка при проверке SL/TP для {symbol}: {e}")

            # --- Обновляем список пар с учётом cooldown ---
            pairs = select_pairs(cfg, risk_guard=risk_guard)

            # --- Обработка сигналов стратегий ---
            for strategy_func, strategy_name in strategies:
                for symbol in pairs:
                    try:
                        ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=ohlcv_limit)
                        if not ohlcv:
                            continue
                        df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
                        signal = strategy_func(df, live_mode=True)
                        if signal not in ["buy", "sell"]:
                            continue
                        last_price = float(df["close"].iloc[-1])
                        logging.info(f"Сигнал {signal.upper()} от {strategy_name} для {symbol} @ {last_price}")
                        executor.execute_trade(
                            symbol=symbol,
                            side=signal,
                            price=last_price,
                            ohlcv_df=df
                        )
                    except Exception as e:
                        logging.error(f"Ошибка при обработке {symbol} стратегией {strategy_name}: {e}")

            logging.info(f"Ожидание {trade_loop_interval} сек...")
            time.sleep(trade_loop_interval)
