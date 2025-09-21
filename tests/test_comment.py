import pandas as pd
from types import SimpleNamespace
from bot_ai.exec.executor import TradeExecutor

def main():
    # Фейковая конфигурация
    cfg = SimpleNamespace()
    cfg.mode = "dry-run"
    cfg.risk = SimpleNamespace(test_equity=1000)

    # ✅ Добавляем фейковую секцию sl_tp, чтобы не падал расчёт SL/TP
    cfg.sl_tp = SimpleNamespace(
        atr_multiplier_sl=1.0,
        atr_multiplier_tp=2.0
    )

    # Фейковые данные OHLCV
    ohlcv_df = pd.DataFrame({
        "high": [120, 121, 122],
        "low": [100, 101, 102],
        "close": [110, 111, 112]
    })

    # Создаём исполнителя сделок
    executor = TradeExecutor(cfg)

    # Открываем сделку с комментарием
    executor.execute_trade(
        "BTC/USDT",
        "buy",
        110.0,
        ohlcv_df,
        comment="Сигнал по EMA crossover"
    )

    print("Сделка выполнена. Проверьте файл data/trades_log.csv")

if __name__ == "__main__":
    main()