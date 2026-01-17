# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/execution/executor.py
# Назначение: Выполнение торговых сигналов через Binance API
# ============================================

from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET

# Глобальный клиент должен быть инициализирован в bot_live.py
client: Client = None

def set_client(binance_client: Client):
    """
    Устанавливает глобальный Binance клиент.
    """
    global client
    client = binance_client

def execute_signal(pair: str, signal: dict):
    """
    Выполняет торговый сигнал: BUY или SELL по рынку.
    """
    if client is None:
        raise RuntimeError("Binance клиент не установлен. Вызови set_client(client) перед использованием.")

    side = signal["side"]
    qty = signal["qty"]

    print(f"🛒 Отправка ордера: {side} {qty} {pair}")

    try:
        order = client.create_order(
            symbol=pair,
            side=SIDE_BUY if side == "BUY" else SIDE_SELL,
            type=ORDER_TYPE_MARKET,
            quantity=qty
        )
        print(f"✅ Ордер выполнен: {order['orderId']}")

    except Exception as e:
        print(f"❌ Ошибка при отправке ордера: {e}")
