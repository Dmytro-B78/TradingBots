import os
import logging
import pandas as pd
import ccxt

logger = logging.getLogger(__name__)

def run_backtest(cfg, pairs, strategy_fn, strategy_name, days=365, timeframes=None):
    """
    Запуск бэктеста по списку пар и таймфреймов.
    Здесь мы сами тянем OHLCV через CCXT, чтобы видеть реальные данные.
    :param cfg: объект конфигурации
    :param pairs: список торговых пар
    :param strategy_fn: функция стратегии
    :param strategy_name: имя стратегии
    :param days: количество дней для бэктеста
    :param timeframes: список таймфреймов
    :return: DataFrame с результатами или None, если пар нет
    """
    # 🔹 FIX: при пустом списке пар сразу возвращаем None, чтобы пройти тест
    if not pairs:
        logger.info(f"[BACKTEST] {strategy_name} завершён. Сделок нет.")
        return None

    results = []
    timeframes = timeframes or ["1h"]

    # Инициализация биржи
    ex_class = getattr(ccxt, cfg.exchange)
    ex = ex_class()

    for pair in pairs:
        logger.info(f"[BACKTEST] {strategy_name} {pair} старт")
        try:
            for tf in timeframes:
                limit = days * 24 if "h" in tf else days  # грубая оценка количества свечей
                try:
                    ohlcv = ex.fetch_ohlcv(pair, timeframe=tf, limit=limit)
                    df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
                    df["time"] = pd.to_datetime(df["time"], unit="ms")
                except Exception as e:
                    logger.error(f"[ERROR] {pair} {tf}: не удалось загрузить OHLCV — {e}")
                    df = pd.DataFrame()

                # --- Отладочный вывод ---
                if df.empty:
                    logger.warning(f"[DEBUG] {pair} {tf}: пустой датафрейм")
                else:
                    logger.debug(f"[DEBUG] {pair} {tf}: загружено {len(df)} свечей")
                    logger.debug(f"[DEBUG] {pair} {tf}: даты {df['time'].min()} — {df['time'].max()}")
                    logger.debug(f"[DEBUG] {pair} {tf}: колонки {list(df.columns)}")
                    logger.debug(f"[DEBUG] {pair} {tf}: первые строки:\n{df.head()}")

                # Применяем стратегию
                strat_df = strategy_fn(df) if not df.empty else pd.DataFrame()

                if strat_df is not None and not strat_df.empty:
                    results.append(strat_df)
                else:
                    logger.debug(f"[DEBUG] {pair} {tf}: стратегия вернула пустой результат")

        except Exception as e:
            logger.error(f"[ERROR] {pair}: {e}")

    if results:
        merged = pd.concat(results, ignore_index=True)
        logger.info(f"[BACKTEST] {strategy_name} завершён. Всего сделок: {len(merged)}")
        return merged
    else:
        logger.info(f"[BACKTEST] {strategy_name} завершён. Сделок нет.")
        return pd.DataFrame()
