# -*- coding: utf-8 -*-
# === bot_ai/strategy/trader.py ===
# Торговый цикл с частичным выходом, трейлинг-стопом и управлением позицией

import csv
import logging
import os
import time
from datetime import datetime

from binance.client import Client
from binance.enums import ORDER_TYPE_MARKET, SIDE_BUY, SIDE_SELL

from bot_ai.risk.position_manager import PositionManager
from bot_ai.risk.risk_manager import RiskManager
from bot_ai.strategy import strategy_selector
from bot_ai.utils.data import fetch_ohlcv
from bot_ai.utils.notifier import Notifier

logger = logging.getLogger(__name__)

# === CSV логирование сделок ===

def save_trade_to_csv(trade: dict, path: str = "trades_log.csv"):
    file_exists = os.path.isfile(path)
    with open(path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=trade.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(trade)

# === Отправка рыночного ордера через Binance ===

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
        logger.info(
            f"[BINANCE] Ордер исполнен: {
                side.upper()} {qty} {symbol} @ {price}")
        return {
            "status": "filled",
            "filled_price": price,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"[BINANCE] Ошибка при размещении ордера: {e}")
        return {"status": "error", "error": str(e)}

# === Основной торговый цикл ===

def run_trading_loop(cfg):
    pair = cfg["symbol"]
    timeframe = cfg.get("timeframe", "1h")
    strategy_name = cfg.get("strategy", "adaptive")

    # Параметры управления позицией
    trailing_sl = cfg.get("trailing_sl", None)
    partial_pct = cfg.get("partial_pct", 0.5)
    move_sl_to_be = cfg.get("move_sl_to_be", True)

    strategy = strategy_selector.get(strategy_name)
    if strategy is None:
        logger.error(f"Стратегия '{strategy_name}' не найдена.")
        return

    risk = RiskManager(cfg)
    notifier = Notifier(cfg)
    position = PositionManager()
    client = Client(cfg["binance_api_key"], cfg["binance_api_secret"])

    while True:
        df = fetch_ohlcv(pair, timeframe=timeframe, limit=100)
        if df is None or df.empty:
            logger.warning("Нет данных для анализа.")
            time.sleep(60)
            continue

        current_price = df["close"].iloc[-1]

        # === Проверка открытой позиции ===
        if position.is_open():
            position.update_trailing_sl(current_price)
            exit_info = position.check_exit(current_price)
            if exit_info:
                logger.info(f"?? ЗАКРЫТИЕ: {exit_info}")
                notifier.trade_close({
                    "Symbol": exit_info["symbol"],
                    "Side": exit_info["side"],
                    "Price": exit_info["exit"],
                    "Profit(%)": exit_info["pnl_pct"],
                    "Profit(USDT)": exit_info["pnl_usdt"]
                })
                save_trade_to_csv(exit_info)
                time.sleep(cfg.get("poll_interval", 60))
                continue

        # === Генерация нового сигнала ===
        signal = strategy.generate_signal(df, cfg)
        if signal is None or signal.get("side") == "flat":
            logger.info("Нет сигнала или flat.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        logger.info(f"Сигнал: {signal}")
        result = risk.execute(signal)
        if result is None:
            logger.info("Сделка отклонена риск-менеджером.")
            notifier.alert("Сделка отклонена риск-менеджером.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        # === Исполнение через Binance ===
        order = place_order_binance(
            client, pair, signal["side"], result["qty"])
        if order["status"] != "filled":
            notifier.alert("Ордер не исполнен.")
            time.sleep(cfg.get("poll_interval", 60))
            continue

        notifier.trade_open({
            "Symbol": pair,
            "Side": signal["side"],
            "Price": order["filled_price"],
            "PositionSize": result["qty"],
            "SL": result["sl"],
            "TP1": result["tp1"],
            "TP2": result["tp2"]
        })

        # === Сохраняем открытую позицию с частичным выходом ===
        position.open(
            symbol=pair,
            side=signal["side"],
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

