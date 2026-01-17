# monitor_main.py
# Назначение: Мониторинг состояния бота и логов
# Структура:
# └── bot_ai/diagnostics/monitor_main.py

from bot_ai.core.state_manager import get_balance, get_positions

def main():
    print("📊 Monitoring Bot State")
    print(f"Balance: {get_balance()}")
    print("Positions:")
    for pos in get_positions():
        print(pos)
