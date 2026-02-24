# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/strategy/trader_engine.py
# Назначение: Live-трейдинг с Binance API, Signal, PositionManager
# Использует: strategy_selector, strategy_router, RiskManager, Notifier
# ============================================

import csv
import logging
import os
import time
from datetime import datetime

from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL

from bot_ai.core.context import MarketContext
from bot_ai.core.signal import Signal
from bot_ai.risk.position_manager import PositionManager
from bot_ai.risk.risk_manager import RiskManager
from bot_ai.strategy import strategy_selector
from bot_ai.strategy.strategy_router import route_strategy
from bot_ai.strategy.strategy_validator import validate_config
from bot_ai.utils.data import fetch_ohlcv
from bot_ai.utils.notifier import Notifier

logger = logging.getLogger(__name__)

def save_trade_to_csv(trade: dict, path: str = "trades_log.csv"):
    file_exists = os.path.isfile(path)
    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=trade.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(trade)

def place_order_binance(client, symbol: str, side: str, qty: float) -> dict:
    try:
        binance_side = SIDE_BUY if side == "long" else SIDE_SELL
        order = client.create_order(
            symbol=symbol.upper(),
            side=binance_side,
            type=ORDER_TYPE_MARKET,
            quantity=qty
        )
        price = float(order["fills"][0]["price"])
        logger.info(f"[BINANCE] Ордер исполнен: {side.upper()} {qty} {symbol} @ {price}")
        return {
            "status": "filled",
            "filled_price": price,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"[BINANCE] Ошибка при размещении ордера: {e}")
        return {"status": "error", "error": str(e)}

def run_trading_loop(cfg):
    try:
        validate_config(cfg)
    except ValueError as e:
        logger.error(f"Ошибка валидации конфигурации: {e}")
        return

    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "adaptive")

    trailing_sl = cfg.get("trailing_sl", None)
    partial_pct = cfg.get("partial_pct", 0.5)
    move_sl_to_be = cfg.get("move_sl_to_be", True)

    client = Client(cfg["binance_api_key"], cfg["binance_api_secret"])
    risk = RiskManager(cfg)
    notifier = Notifier(cfg)
    position = PositionManager()

    logger.info(f"Старт стратегии: {strategy_name} | Пара: {pair} | Таймфрейм: {timeframe}")

    while True:
        df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            logger.warning("Нет данных OHLCV. Повтор через 60 секунд.")
            time.sleep(60)
            continue

        context = MarketContext(df=df, symbol=pair, time=datetime.utcnow())

        if strategy_name == "adaptive":
            strategy = route_strategy(df, config={})
        else:
            strategy = strategy_selector.get(strategy_name)
            if strategy is None:
                logger.error(f"Стратегия '{strategy_name}' не найдена.")
                return

        if not hasattr(strategy, "generate_signal"):
            logger.error(f"Стратегия '{strategy_name}' не реализует метод generate_signal(context).")
            return

        signal = strategy.generate_signal(context)

        if not isinstance(signal, Signal):
            logger.info("Нет сигнала от стратегии.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        logger.info(f"Сигнал: {signal}")
        current_price = df["close"].iloc[-1]

        if position.is_open():
            position.update_trailing_sl(current_price)
            exit_info = position.check_exit(current_price)
            if exit_info:
                logger.info(f"Выход из позиции: {exit_info}")
                notifier.trade_close(exit_info)
                save_trade_to_csv(exit_info)
                time.sleep(cfg.get("poll_interval", 60))
                continue

        result = risk.execute(signal)
        if result is None:
            logger.info("Сигнал отклонён RiskManager.")
            notifier.alert("Сигнал отклонён RiskManager.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        order = place_order_binance(client, pair, signal.side, result["qty"])
        if order["status"] != "filled":
            notifier.alert("Ошибка при размещении ордера.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        notifier.trade_open({
            "Symbol": pair,
            "Side": signal.side,
            "Price": order["filled_price"],
            "PositionSize": result["qty"],
            "SL": result["sl"],
            "TP1": result["tp1"],
            "TP2": result["tp2"]
        })

        position.open(
            symbol=pair,
            side=signal.side,
            entry=order["filled_price"],
            sl=result["sl"],
            tp1=result["tp1"],
            tp2=result["tp2"],
            qty=result["qty"],
            strategy=strategy_name,
            trailing_sl=trailing_sl,
            partial_pct=partial_pct,
            move_sl_to_be=move_sl_to_be
        )

        time.sleep(cfg.get("poll_interval", 60))
