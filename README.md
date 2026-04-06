# ================================================================
# NT-Tech Trading Engine 3.x (Spot Only, Long Only)
# ASCII-only
# ================================================================

A modular, deterministic, ASCII-only trading engine for spot-only
algorithmic trading under strict NT-Tech Mode rules.

Core capabilities:
- Ultra-fast backtesting (2,000,000+ candles/sec)
- Live trading (LiveEngine 3.x, Binance API)
- Strict Mode C execution safety
- Market scanning (USDT pairs, volume >= 50M)
- Regime-aware MetaStrategy 4.x
- Volatility-adaptive consensus engine
- Entry-only anti-whipsaw filtering
- Deterministic logging (FileLogger 3.0)
- Dry-run mode for safe testing

All modules follow NT-Tech Mode:
- ASCII-only
- Full-file PowerShell blocks
- No Cyrillic
- Deterministic formatting
- Ready for direct execution

------------------------------------------------
Directory Structure
------------------------------------------------

C:\TradingBots\NT\
│   main.py
│   config.json
│   README.md
│   CHANGELOG.md
│
├── bot_ai\
│   ├── config\
│   │     config.py
│   │
│   └── engine\
│         backtest_engine.py
│         live_engine.py
│         data_loader.py
│         file_logger.py
│         utils.py
│         risk_manager.py (stub)
│         strategy_router.py
│         config_loader.py
│         trade_analyzer.py
│         __init__.py
│
└── bot_ai\
    └── strategy\
          meta_strategy.py (MetaStrategy 4.5.4)
          ma_crossover_strategy.py
          rsi_strategy.py
          macd_strategy.py
          bollinger_strategy.py
          microtrend_strategy.py

------------------------------------------------
MetaStrategy 4.5.4 (Current Stable)
------------------------------------------------

MetaStrategy 4.5.4 is a regime-aware, volatility-adaptive
consensus engine for long-only spot trading.

Key properties:

- Regime detection:
    trend
    range
    expansion
    compression

- Compression behavior:
    * entries blocked
    * exits always allowed

- Volatility Engine (ATR-based):
    * hard ATR gate for entries
    * adaptive strategy weights
    * adaptive open/close thresholds

- Consensus model:
    * weighted multi-strategy voting
    * regime-aware normalization
    * EMA-smoothed confidence

- Anti-whipsaw:
    * applied to entries only
    * never blocks exits
    * directional momentum boost

Signal model:
    OPEN_LONG
    CLOSE_LONG

------------------------------------------------
Backtest Engine 3.x
------------------------------------------------

- Spot-only, Long-only
- Deterministic candle ordering
- Equity curve
- Sharpe ratio
- Max drawdown
- Trade log
- ASCII-only output

------------------------------------------------
Live Engine 3.x (Strict Mode C)
------------------------------------------------

- Official binance-connector client
- Market scanner (USDT pairs, volume >= 50M)
- Real-time price feed
- Market buy/sell execution
- Long-only
- Position sizing by percentage of USDT balance
- ATR SL/TP enforcement
- Dry-run mode

Strict Mode C safety:
- allow_live_trading loaded ONLY from config.json
- dry_run can be overridden from scripts
- real trading requires BOTH:
    allow_live_trading = true
    dry_run = false
- fail-safe blocks all real orders if allow_live_trading = false

------------------------------------------------
Logs
------------------------------------------------

All logs are written to:
C:/TradingBots/NT/logs/live_log.txt

------------------------------------------------
End of README
------------------------------------------------
