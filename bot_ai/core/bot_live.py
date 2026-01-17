# bot_live.py
# Назначение: Запуск бота в live‑режиме с реальными ордерами
# Структура:
# └── bot_ai/core/bot_live.py

from strategy_config_loader import load_config
from bot_ai.selector.selector_engine import run_selector
from bot_ai.exchange.data_loader import load_ohlcv
from bot_ai.exec.risk_guard import is_trade_allowed
from bot_ai.exec.order_executor import execute_order
from bot_ai.exec.trade_logger import log_trade

def main():
    config = load_config()
    symbol = "BTC/USDT"
    df = load_ohlcv(symbol, limit=100)

    trades = run_selector(symbol, df, config)
    for trade in trades:
        if is_trade_allowed(trade, config):
            result = execute_order(**trade)
            log_trade(result)
