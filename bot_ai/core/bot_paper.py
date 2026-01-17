# bot_paper.py
# Назначение: Запуск бота в режиме paper‑трейдинга (без реальных ордеров)
# Структура:
# └── bot_ai/core/bot_paper.py

from strategy_config_loader import load_config
from bot_ai.selector.selector_engine import run_selector
from bot_ai.exchange.data_loader import load_ohlcv
from bot_ai.exec.risk_guard import is_trade_allowed
from bot_ai.exec.trade_logger import log_trade
from bot_ai.core.state_manager import add_position

def main():
    config = load_config()
    symbol = "BTC/USDT"
    df = load_ohlcv(symbol, limit=100)

    trades = run_selector(symbol, df, config)
    for trade in trades:
        if is_trade_allowed(trade, config):
            add_position(trade)
            log_trade(trade)
