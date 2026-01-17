<<<<<<< HEAD
﻿# ============================================
# ✅ backtest_engine.py — движок бэктеста
# Обновление:
# - Загрузка исторических данных
# - Вызов strategy.load_data(df)
# - Вызов strategy.generate_signals()
# Расположение: bot_ai/backtest/backtest_engine.py
# ============================================
=======
<<<<<<< Updated upstream
﻿import ccxt
import pandas as pd
import os
import logging
from datetime import datetime, timedelta
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

from bot_ai.risk.risk_manager import RiskManager
from bot_ai.utils.data import load_ohlcv  # ← функция загрузки данных

def run_backtest(cfg, pairs, strategy_fn, strategy_name, days, timeframes):
    results = {}

    # ✅ Гарантируем, что cfg — это dict
    cfg_dict = cfg if isinstance(cfg, dict) else vars(cfg)
    risk_manager = RiskManager(cfg_dict)

    for pair in pairs:
        results[pair] = {}
        for tf in timeframes:
            # ⏳ Загружаем исторические данные
            df = load_ohlcv(pair, tf, days)
            if df is None or df.empty:
                results[pair][tf] = None
                continue

            # ⚙️ Инициализируем стратегию и подаём данные
            strategy = strategy_fn(cfg_dict, pair=pair, timeframe=tf)
            strategy.load_data(df)
            strategy.generate_signals()

            # 🚀 Запускаем бэктест
            stats = strategy.run_backtest()
            results[pair][tf] = stats

<<<<<<< HEAD
    return results
=======
    summary = []
    for symbol in pairs:
        try:
            # Сохраняем OHLCV для каждого таймфрейма
            for tf in timeframes:
                since = exchange.parse8601((datetime.utcnow() - timedelta(days=days)).isoformat())
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=tf, since=since, limit=days*24)
                if not ohlcv:
                    continue

                df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
                ohlcv_file = os.path.join(results_dir, f"{symbol.replace('/', '_')}_{tf}_ohlcv.csv")
                df.to_csv(ohlcv_file, index=False)

                # Запускаем стратегию только на основном таймфрейме (например, 1h)
                if tf == timeframes[0]:
                    trades = strategy_func(df)

                    # Применяем RiskGuard и SL/TP к сделкам
                    filtered_trades = []
                    for _, trade in trades.iterrows():
                        if not risk_guard.can_open_trade(symbol):
                            logger.info(f"RiskGuard: сделка по {symbol} отклонена")
                            continue

                        size = position_sizer.calculate(symbol, trade)
                        sl, tp = sltp_calc.calculate(df, trade)

                        trade_data = trade.to_dict()
                        trade_data["PositionSize"] = size
                        trade_data["SL"] = sl
                        trade_data["TP"] = tp
                        filtered_trades.append(trade_data)

                        risk_guard.register_trade(symbol, trade_data)

                    trades_df = pd.DataFrame(filtered_trades)
                    trades_file = os.path.join(results_dir, f"{symbol.replace('/', '_')}_trades.csv")
                    trades_df.to_csv(trades_file, index=False)

                    total_profit = trades_df['Profit(%)'].sum(skipna=True) if 'Profit(%)' in trades_df.columns else 0
                    summary.append((symbol, len(trades_df)//2, total_profit))

        except Exception as e:
            logger.warning(f"Ошибка backtest для {symbol}: {e}")

    summary_df = pd.DataFrame(summary, columns=['Symbol', 'Trades', 'TotalProfit(%)'])
    summary_file = os.path.join(results_dir, "summary.csv")
    summary_df.to_csv(summary_file, index=False)

    logger.info(f"Backtest '{strategy_name}' завершён. Результаты в {results_dir}")
=======
﻿# ============================================
# ✅ backtest_engine.py — движок бэктеста
# Обновление:
# - Загрузка исторических данных
# - Вызов strategy.load_data(df)
# - Вызов strategy.generate_signals()
# Расположение: bot_ai/backtest/backtest_engine.py
# ============================================

from bot_ai.risk.risk_manager import RiskManager
from bot_ai.utils.data import load_ohlcv  # ← функция загрузки данных

def run_backtest(cfg, pairs, strategy_fn, strategy_name, days, timeframes):
    results = {}

    # ✅ Гарантируем, что cfg — это dict
    cfg_dict = cfg if isinstance(cfg, dict) else vars(cfg)
    risk_manager = RiskManager(cfg_dict)

    for pair in pairs:
        results[pair] = {}
        for tf in timeframes:
            # ⏳ Загружаем исторические данные
            df = load_ohlcv(pair, tf, days)
            if df is None or df.empty:
                results[pair][tf] = None
                continue

            # ⚙️ Инициализируем стратегию и подаём данные
            strategy = strategy_fn(cfg_dict, pair=pair, timeframe=tf)
            strategy.load_data(df)
            strategy.generate_signals()

            # 🚀 Запускаем бэктест
            stats = strategy.run_backtest()
            results[pair][tf] = stats

    return results
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
