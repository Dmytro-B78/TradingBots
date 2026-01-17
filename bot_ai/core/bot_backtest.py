# bot_backtest.py
# Назначение: Прогон стратегии на исторических данных
# Структура:
# └── bot_ai/core/bot_backtest.py

from strategy_config_loader import load_config
from bot_ai.selector.selector_engine import run_selector
from bot_ai.exchange.data_loader import load_ohlcv

def main():
    config = load_config()
    symbol = "BTC/USDT"
    df = load_ohlcv(symbol, limit=500)

    trades = run_selector(symbol, df, config)

    print(f"📈 Бэктест завершён. Сигналов: {len(trades)}")
    for t in trades:
        print(f"{t['strategy']} | {t['side']} | entry={t['entry']:.2f} | target={t['target']:.2f}")

if __name__ == "__main__":
    main()
