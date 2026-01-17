# ============================================
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
