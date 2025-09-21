import ccxt
import pandas as pd
import os
import logging
from datetime import datetime, timedelta

from bot_ai.risk.guard import RiskGuard
from bot_ai.risk.position_sizer import PositionSizer
from bot_ai.risk.dynamic_sl_tp import DynamicSLTP

def run_backtest(cfg, pairs, strategy_func, strategy_name, days=30, timeframes=None):
    logger = logging.getLogger(__name__)
    if not pairs:
        logger.warning("Список пар пуст — backtest не запущен.")
        return

    if timeframes is None:
        timeframes = ["1h", "4h", "1d"]

    ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
    results_dir = os.path.join("data", "backtests", f"{strategy_name}_{ts}")
    os.makedirs(results_dir, exist_ok=True)

    exchange_class = getattr(ccxt, cfg.exchange)
    exchange = exchange_class({'enableRateLimit': True})

    # Инициализация RiskGuard, PositionSizer и SL/TP
    risk_guard = RiskGuard(cfg)
    position_sizer = PositionSizer(cfg)
    sltp_calc = DynamicSLTP(cfg)

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
