# ============================================
# File: bot_ai/live_trader_engine.py
# Purpose: Execute live or paper trades using selected strategy
# Format: UTF-8 without BOM
# Compatible with Binance Testnet and adaptive strategy routing
# ============================================

import logging
import time
from binance.client import Client
from bot_ai.data_loader import get_binance_ohlcv
from bot_ai.state.position_tracker import PositionTracker
from bot_ai.strategy.strategy_router import get_strategy, route_strategy

# === Main trading loop ===
def run_trading_loop(cfg):
    symbol = cfg["symbol"]
    timeframe = cfg.get("interval", "1h")
    capital = cfg.get("initial_balance", 1000)
    risk_per_trade = cfg.get("risk_per_trade", 0.01)
    stop_loss_pct = cfg.get("stop_loss_pct", 0.01)
    trailing_stop_pct = cfg.get("trailing_stop_pct", None)
    adaptive = cfg.get("strategy") == "adaptive"
    qty = cfg.get("qty", 0.001)
    lookback = cfg.get("lookback_candles", 150)

    # === Load historical candles ===
    df = get_binance_ohlcv(symbol, timeframe, limit=lookback)
    if df is None or df.empty:
        logging.error(f"[DATA] Failed to load candles for {symbol}")
        return

    # === Select strategy ===
    if adaptive:
        strategy = route_strategy(df, cfg)
    else:
        strategy = get_strategy(cfg["strategy"], cfg)

    # === Generate signal ===
    signal = strategy.generate_signal(df)
    if not signal:
        logging.info(f"[{symbol}] No signal generated.")
        return

    logging.info(f"[{symbol}] Signal: {signal.action} @ {signal.price}")

    # === Position tracking ===
    tracker = PositionTracker(symbol, timeframe)
    open_pos = tracker.load()

    # === Execute BUY ===
    if signal.action.upper() == "BUY" and not open_pos:
        logging.info(f"[{symbol}] Executing BUY at {signal.price} for qty={qty}")
        if cfg["mode"] == "live":
            client = Client(cfg["api_key"], cfg["api_secret"], testnet=True)
            client.order_market_buy(symbol=symbol, quantity=qty)
        tracker.save(signal.time, signal.price)

    # === Execute SELL ===
    elif signal.action.upper() == "SELL" and open_pos:
        logging.info(f"[{symbol}] Executing SELL at {signal.price}")
        if cfg["mode"] == "live":
            client = Client(cfg["api_key"], cfg["api_secret"], testnet=True)
            client.order_market_sell(symbol=symbol, quantity=qty)
        tracker.clear()

    # === No trade executed ===
    else:
        logging.info(f"[{symbol}] No trade executed. Signal={signal.action}, Open={bool(open_pos)}")
