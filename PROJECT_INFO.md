# ================================================================
# NT-Tech Trading Engine 4.x
# PROJECT INFORMATION (ASCII-only)
# ================================================================

Project Name:
    NT-Tech Trading Engine (Spot Only, Long Only)

Version:
    Core Engine: 4.x
    MetaStrategy: 8.4-M-F
    RiskEngine: 1.0
    PositionManager: 2.3
    LiveEngine: 4.1
    OfflineRunner: 7.6-F

Execution Model:
    Spot-only
    Long-only
    Deterministic
    No leverage
    No shorts
    Strict Mode C safety
    Intrabar-aware exits (synthetic)

================================================
System Overview
================================================

The NT-Tech Trading Engine is a modular, deterministic,
ASCII-only trading system designed for high-performance
algorithmic trading under strict reproducibility rules.

The system consists of:
- MetaStrategy 8.4-M-F (modular, ATR-aware, intrabar stops)
- RiskEngine 1.0 (institutional risk module)
- PositionManager 2.3 (position state, stops, PnL)
- LiveEngine 4.1 (signal + risk integration)
- OfflineRunner 7.6-F (intrabar-aware CSV diagnostics)
- BacktestEngine 3.x (deterministic backtesting)

All modules follow NT-Tech Mode:
- ASCII-only
- Full-file PowerShell blocks
- No Cyrillic
- Deterministic formatting
- Ready for direct execution

================================================
MetaStrategy 8.4-M-F Overview
================================================

MetaStrategy 8.4-M-F is a modular, multi-stage trading engine
with synthetic intrabar stop execution for 1h candles.

Pipeline:
1) Indicator Engine
   - EMA(30/90/180)
   - ATR(1h/4h)
   - Momentum, slope, trend strength
   - ATR mean tracking

2) Regime Engine
   - ATR regimes (low/normal/high)
   - Local regime (trend/range/expansion)
   - Global regime (trend/range/expansion)
   - MTF bias (1h + synthetic 4h)

3) Stage 1 (High Recall)
   - Trend, slope, momentum gates
   - Confidence smoothing
   - EMA structure filter

4) Stage 2 (High Precision)
   - MTF bias gate
   - ATR regime gate
   - Impulse window
   - Structure validation

5) Intrabar Stop Engine (synthetic)
   - Absolute stop (-6 percent)
   - HWM drawdown stop (-6 percent)
   - ATR trailing stop
   - EMA-ATR stop
   - All stops evaluated using candle.low
   - exit_price propagated to OfflineRunner

6) Soft Exit Engine
   - Confidence drop
   - Regime flip
   - Momentum loss
   - Trend flip
   - High volatility exit

================================================
RiskEngine 1.0
================================================

- ATR-based stop distance
- Volatility-aware stop multipliers
- Volatility shock protection
- Dynamic risk scaling (local + global regime)
- MTF bias influence
- Max exposure control
- Daily/weekly loss limits
- Kill-switch (disabled in offline mode)

================================================
OfflineRunner 7.6-F
================================================

Key features:
- Intrabar-aware exit_price support
- Synthetic intrabar stop execution
- Deterministic CSV processing
- Compact meta_signal and trade logs
- Full compatibility with Analyzer 2.1

Exit logic:
- If MetaStrategy returns exit_price -> use it
- Else fallback to close_price

================================================
Directory Structure (Updated)
================================================

C:\TradingBots\NT
│   README.md
│   PROJECT_INFO.md
│   CHANGELOG.md
│   config.json
│   main.py
│   ...
│
├── bot_ai
│   ├── strategy
│   │     meta_strategy.py        (thin wrapper)
│   │     filters.py
│   │     ...
│   │     meta/
│   │         __init__.py
│   │         indicators.py
│   │         regimes.py
│   │         stage1.py
│   │         stage2.py
│   │         intrabar_stops.py
│   │         exits.py
│   │         meta_strategy.py    (core 8.4-M-F)
│   │
│   ├── engine
│   │     offline_runner.py       (7.6-F)
│   │     live_engine.py
│   │     ...
│   │
│   ├── risk
│   │     risk_guard.py
│   │
│   ├── backtest
│   │     backtest_engine.py
│   │
│   └── common
│         indicators.py
│         utils.py

================================================
Execution Modes
================================================

Offline Mode:
- Uses OfflineRunner 7.6-F
- Intrabar stops enabled
- No API calls
- kill-switch disabled

Live Mode:
- Requires allow_live_trading = true
- dry_run = false
- kill-switch optional
- Intrabar stops disabled (exchange-level execution required)

================================================
Logging
================================================

All logs are ASCII-only and deterministic.

Default paths:
C:/TradingBots/NT/logs/live_log.txt
C:/TradingBots/NT/logs/backtest_log.txt
C:/TradingBots/NT/logs/offline_log.txt

================================================
End of PROJECT_INFO
================================================
