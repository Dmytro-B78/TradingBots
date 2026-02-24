# ============================================
# Path: C:\TradingBots\NT\tests\test_exchange_interface.py
# Purpose: Pytest test for Exchange mock interface
# Format: UTF-8 without BOM
# ============================================

import pytest
from bot_ai.core.exchange_interface import Exchange

@pytest.fixture
def exchange():
    return Exchange(api_key="test-key", api_secret="test-secret")

def test_place_order(exchange):
    order = exchange.place_order(
        symbol="ETH/USDT",
        side="sell",
        price=3000,
        size=0.5,
        stop=2900,
        target=3200
    )
    assert order["symbol"] == "ETH/USDT"
    assert order["side"] == "sell"
    assert order["price"] == 3000
    assert order["status"] == "placed"

def test_cancel_order(exchange):
    result = exchange.cancel_order(order_id="test-order-456")
    assert result["order_id"] == "test-order-456"
    assert result["status"] == "cancelled"
