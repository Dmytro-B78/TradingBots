# -*- coding: utf-8 -*-
# === config.py ===
# Configuration for the "adaptive" strategy

cfg = {
    "strategy": "adaptive",           # Strategy name
    "symbol": "BTC/USDT",             # Trading pair
    "timeframe": "1h",                # Candle interval

    # Indicator parameters
    "ema_fast": 5,                    # Fast EMA period
    "ema_slow": 20,                   # Slow EMA period
    "rsi_period": 14,                 # RSI period

    # Stop-loss and take-profit settings
    "sl_tp": {
        "sl_type": "atr",             # "atr" or "percent"
        "sl_value": 1.0,              # 1 ATR or 1%
        "tp_type": "r_multiple",      # "r_multiple" or "percent"
        "tp_value": 2.0               # 2R or 2%
    },

    "poll_interval": 60              # Time between market checks (in seconds)
}

