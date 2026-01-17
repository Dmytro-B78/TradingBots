# debug_tools.py
# Назначение: Утилиты для отладки и визуализации
# Структура:
# └── bot_ai/diagnostics/debug_tools.py

import matplotlib.pyplot as plt

def plot_equity_curve(equity):
    plt.plot(equity)
    plt.title("📈 Equity Curve")
    plt.xlabel("Trade #")
    plt.ylabel("Balance")
    plt.grid(True)
    plt.show()

def print_trade_summary(trades):
    for i, t in enumerate(trades):
        print(f"{i+1:02d}) {t['side']} {t['symbol']} @ {t['entry']} → {t['target']} / SL {t['stop']}")
