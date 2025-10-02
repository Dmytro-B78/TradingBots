import os
import logging
import pandas as pd
import ccxt

# 🔹 Импорты для тестов — чтобы monkeypatch мог подменять классы
from bot_ai.risk.risk_guard import RiskGuard
from bot_ai.risk.position_sizer import PositionSizer
from bot_ai.risk.dynamic_sl_tp import DynamicSLTP

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
    :return: DataFrame с результатами или None, если сделок нет
    """
    # 🔹 FIX: при пустом списке пар сразу возвращаем None
    if not pairs:
        logger.info(f"[BACKTEST] {strategy_name} завершён. Сделок нет.")
        return None

    results = []
    timeframes = timeframes or ["1h"]

    # Инициализация биржи
    ex_class = getattr(ccxt, cfg.exchange)
    ex = ex_class()

    # Инициализация риск‑модулей
    rg = RiskGuard(cfg)
    ps = PositionSizer(cfg)
    sltp = DynamicSLTP(cfg)

    for pair in pairs:
        logger.info(f"[BACKTEST] {strategy_name} {pair} старт")
        try:
            for tf in timeframes:
                limit = days * 24 if "h" in tf else days
                try:
                    ohlcv = ex.fetch_ohlcv(pair, timeframe=tf, since=None, limit=limit)
                    df = pd.DataFrame(ohlcv, columns=["time", "open", "high", "low", "close", "volume"])
                    df["time"] = pd.to_datetime(df["time"], unit="ms")
                except Exception as e:
                    logger.error(f"[ERROR] {pair} {tf}: не удалось загрузить OHLCV — {e}")
                    df = pd.DataFrame()

                if df.empty:
                    logger.warning(f"[DEBUG] {pair} {tf}: пустой датафрейм")
                else:
                    logger.debug(f"[DEBUG] {pair} {tf}: загружено {len(df)} свечей")
                    logger.debug(f"[DEBUG] {pair} {tf}: даты {df['time'].min()} — {df['time'].max()}")
                    logger.debug(f"[DEBUG] {pair} {tf}: колонки {list(df.columns)}")
                    logger.debug(f"[DEBUG] {pair} {tf}: первые строки:\n{df.head()}")

                strat_df = strategy_fn(df) if not df.empty else pd.DataFrame()

                # 🔹 Фильтрация сделок через RiskGuard
                if strat_df is not None and not strat_df.empty:
                    filtered_trades = []
                    for _, trade in strat_df.iterrows():
                        if rg.can_open_trade(pair):
                            size = ps.calculate(pair, trade)
                            sl, tp = sltp.calculate(df, trade)
                            rg.register_trade(pair, trade)
                            # Можно добавить trade в итог, если нужно
                            filtered_trades.append(trade)
                    if filtered_trades:
                        results.append(pd.DataFrame(filtered_trades))
                    else:
                        logger.debug(f"[DEBUG] {pair} {tf}: все сделки отклонены RiskGuard/PositionSizer/DynamicSLTP")
                else:
                    logger.debug(f"[DEBUG] {pair} {tf}: стратегия вернула пустой результат")

        except Exception as e:
            logger.error(f"[ERROR] {pair}: {e}")

    if results:
        merged = pd.concat(results, ignore_index=True)
        if merged.empty:
            logger.info(f"[BACKTEST] {strategy_name} завершён. Сделок нет.")
            return None
        logger.info(f"[BACKTEST] {strategy_name} завершён. Всего сделок: {len(merged)}")
        return merged
    else:
        logger.info(f"[BACKTEST] {strategy_name} завершён. Сделок нет.")
        return None
