# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/execution/trade_logger.py
# Назначение: Логирование исполненных сделок
# Используется в executor.py для вывода информации о сделке
# ============================================

from datetime import datetime

def log_trade(trade: dict):
    """
    Логирует информацию о совершённой сделке в консоль.
    :param trade: словарь с ключами: side, symbol, entry, target, stop
    """
    timestamp = datetime.utcnow().isoformat()
    side = trade.get("side", "-").upper()
    symbol = trade.get("symbol", "-")
    entry = trade.get("entry", "-")
    target = trade.get("target", "-")
    stop = trade.get("stop", "-")

    print(f"📝 LOG [{timestamp}] {side} {symbol} @ {entry} → TP: {target} / SL: {stop}")
