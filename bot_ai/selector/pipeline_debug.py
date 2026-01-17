# pipeline_debug.py
# Назначение: Отладочный запуск селектора с логами
# Структура:
# └── bot_ai/selector/pipeline_debug.py

import pandas as pd
from strategy_config_loader import load_config
from bot_ai.selector.selector_engine import run_selector

def load_mock_data():
    # Пример: 100 свечей с ценой close
    return pd.DataFrame({
        "close": [100 + i * 0.5 for i in range(100)]
    })

def main():
    config = load_config()
    df = load_mock_data()
    symbol = "BTC/USDT"

    trades = run_selector(symbol, df, config)

    print(f"🔍 Найдено {len(trades)} сигналов:")
    for t in trades:
        print(f"{t['strategy']} | {t['side']} | entry={t['entry']:.2f} | size={t['size']}")

if __name__ == "__main__":
    main()
