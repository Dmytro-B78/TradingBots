# ============================================
# Path: C:\TradingBots\NT\tests\demo_exchange_usage.py
# Purpose: Demo usage of Exchange mock interface
# Format: UTF-8 without BOM
# ============================================

from bot_ai.core.exchange_interface import Exchange

def main():
    exchange = Exchange(api_key="demo-key", api_secret="demo-secret")

    # Пример размещения ордера
    order = exchange.place_order(
        symbol="BTC/USDT",
        side="buy",
        price=42000,
        size=0.01,
        stop=41000,
        target=44000
    )
    print("Order placed:", order)

    # Пример отмены ордера
    cancel = exchange.cancel_order(order_id="mock-order-id-123")
    print("Order cancelled:", cancel)

if __name__ == "__main__":
    main()
