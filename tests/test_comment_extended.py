import pandas as pd
from types import SimpleNamespace
from bot_ai.exec.executor import TradeExecutor
import time

def main():
    cfg = SimpleNamespace()
    cfg.mode = "dry-run"
    cfg.risk = SimpleNamespace(test_equity=1000)
    cfg.sl_tp = SimpleNamespace(
        atr_multiplier_sl=1.0,
        atr_multiplier_tp=2.0
    )

    ohlcv_df = pd.DataFrame({
        "high": [120, 121, 122],
        "low": [100, 101, 102],
        "close": [110, 111, 112]
    })

    executor = TradeExecutor(cfg)

    # Открытие позиции
    executor.execute_trade(
        "BTC/USDT",
        "buy",
        110.0,
        ohlcv_df,
        comment="Сигнал по EMA crossover"
    )

    # Делаем паузу, чтобы запись точно попала в файл
    time.sleep(0.5)

    # Закрытие позиции
    executor.execute_trade(
        "BTC/USDT",
        "sell",
        115.0,
        ohlcv_df,
        comment="Выход по сигналу RSI"
    )

    print("Открытие и закрытие позиции выполнены. Проверьте data/trades_log.csv")

if __name__ == "__main__":
    main()
# --- Автопроверка: нет лишнего заголовка в середине trades_log.csv ---
from tests.test_no_header_in_middle import test_no_header_in_middle
test_no_header_in_middle()
