# ================================================================
# NT-Tech Trading Engine 4.x (Spot Only, Long Only)
# ASCII-only
# ================================================================

A modular, deterministic, ASCII-only trading engine for spot-only
algorithmic trading under strict NT-Tech Mode rules.

Core capabilities:
- Ultra-fast backtesting (2,000,000+ candles/sec)
- Live trading (LiveEngine 4.x, Binance API or offline mode)
- Strict Mode C execution safety
- MetaStrategy 9.1-MF (Stage1-Lite, Stage2-Lite v2, Stage 2.2 MetaSignalFilter)
- Volatility-adaptive consensus engine
- Entry-only anti-whipsaw filtering
- Institutional RiskEngine 1.0 (ATR, exposure, loss limits, kill-switch)
- Institutional PositionManager 2.x (stops, trailing, PnL, exposure)
- Full JSONL logging (meta, risk, trades, diagnostics)
- Dry-run mode for safe testing
- OfflineRunner 7.6-F for CSV-based diagnostics

All modules follow NT-Tech Mode:
- ASCII-only
- Full-file PowerShell blocks
- No Cyrillic
- Deterministic formatting
- Ready for direct execution

------------------------------------------------
Directory Structure (Updated)
------------------------------------------------

C:\TradingBots\NT
│   .env
│   .gitignore
│   .nt_tech_ok
│   build_structure.ps1
│   candles.json
│   CHANGELOG.md
│   CHAT_STYLE.md
│   config.json
│   main.py
│   PROJECT_INFO.md
│   README.md
│   test_run_meta.py
│
├── algos
│       mean_reversion_strategy.py
│       rsi_macd.py
│
├── backtest
│       night_backtest.py
│
├── backtest_logs
│
├── bot_ai
│   │   __init__.py
│   │
│   ├── backtest
│   │       backtest_engine.py
│   │
│   ├── common
│   │       indicators.py
│   │       logger.py
│   │       utils.py
│   │
│   ├── config
│   │       backtest_config.json
│   │       config.py
│   │       live_config.json
│   │       optimizer_config.json
│   │       strategy.json
│   │       __init__.py
│   │
│   ├── data
│   │       data_loader.py
│   │       mtf_aggregator.py
│   │
│   ├── engine
│   │       backtest_engine.py
│   │       config_loader.py
│   │       data_loader.py
│   │       file_logger.py
│   │       indicators.py
│   │       indicators_advanced.py
│   │       live_engine.py
│   │       live_loop.py
│   │       logger.py
│   │       offline_runner.py          (7.6-F, intrabar-aware)
│   │       optimizer.py
│   │       optimizer_engine.py
│   │       optimizer_report.py
│   │       order_engine.py
│   │       risk_manager.py
│   │       signal_logger.py
│   │       strategy_router.py
│   │       trade_analyzer.py
│   │       __init__.py
│   │
│   ├── execution
│   │       risk_engine.py
│   │       __init__.py
│   │
│   └── strategy
│           meta_strategy.py           (thin wrapper)
│           filters.py
│           ma_crossover_strategy.py
│           rsi_strategy.py
│           macd_strategy.py
│           bollinger_strategy.py
│           microtrend_strategy.py
│           breakout_strategy.py
│           mean_reversion_strategy.py
│           rsi_macd_strategy.py
│           meta/
│               __init__.py
│               indicators.py
│               regimes.py
│               stage1.py
│               stage2.py
│               meta_signal_filter.py   (Stage 2.2)
│               intrabar_stops.py
│               exits.py
│               meta_strategy.py        (core MetaStrategy 9.1-MF)
│
├── data
│       raw/
│       processed/
│
├── logs
│       live_log.txt
│       backtest_log.txt
│       offline_log.txt
│
└── scripts
        run_dry.ps1
        run_backtest.ps1
        test_meta_strategy_debug.ps1

------------------------------------------------
MetaStrategy 9.1-MF (Adaptive, ATR-aware, Intrabar Stops)
------------------------------------------------

MetaStrategy 9.1-MF is a modular, multi-stage trading engine
with synthetic intrabar stop execution for 1h candles and
adaptive, volatility-aware filters.

Core file:
    C:\TradingBots\NT\bot_ai\strategy\meta\meta_strategy.py

Pipeline:
1) Indicator Engine
   - EMA(10/30/90)
   - ATR(1h/4h)
   - Momentum, slope, trend strength
   - ATR mean tracking

2) Regime Engine
   - ATR regimes (low/normal/high)
   - Local regime (1h)
   - Global regime (4h)
   - MTF bias (synthetic 4h, mtf_bias_4h)

3) Stage 1 (High Recall, Adaptive Filters)
   - Trend, slope, momentum gates
   - Confidence model (NT-Tech 2026)
   - EMA structure filter
   - ATR and regime-aware entry filters

4) Stage 2 (High Precision, Adaptive Filters)
   - MTF bias gate (mtf_bias_4h)
   - ATR regime gate
   - Impulse window
   - Structure validation
   - Soft EMA-based protection for late entries

5) Stage 2.2 — MetaSignalFilter (NEW)
   - EMA smoothing of confidence
   - Hysteresis for OPEN_LONG / CLOSE_LONG
   - 2-bar exit confirmation
   - Noise suppression
   - Unified behavior for LiveEngine and OfflineRunner
   - Stateful filter with deterministic transitions

6) Intrabar Stop Engine (synthetic)
   - Absolute stop (-6 percent)
   - HWM drawdown stop (-6 percent)
   - ATR trailing stop
   - EMA-fast stop (soft intrabar EMA stop)
   - All stops evaluated using candle.low
   - exit_price propagated to OfflineRunner

7) Soft Exit Engine
   - Confidence drop
   - Regime flip
   - Momentum loss
   - Trend flip
   - High volatility exit

Signal model:
    OPEN_LONG
    CLOSE_LONG

------------------------------------------------
Institutional Risk Engine 1.0
------------------------------------------------

RiskEngine is a pure risk module (no order execution).

Core features:
- ATR-based stop distance (1h)
- Volatility-aware stop multipliers
- Volatility shock protection
- Dynamic risk scaling
- Max exposure control
- Daily/weekly loss limits
- Kill-switch

------------------------------------------------
Institutional PositionManager 2.x
------------------------------------------------

Responsibilities:
- Track position (spot LONG only)
- Apply RiskEngine sizing and stops
- Maintain:
    entry_price
    size
    notional
    hard stop
    trailing stop
- Apply exits:
    STOP_LOSS
    TRAILING_STOP
    META_CLOSE
- Track realized PnL
- Optional kill-switch

------------------------------------------------
OfflineRunner 7.6-F (CSV Diagnostics)
------------------------------------------------

- Reads raw Binance kline CSV (no header)
- Intrabar-aware exit_price support
- Synthetic intrabar stop execution
- Deterministic offline diagnostics
- Outputs:
    meta_signal events
    risk_action events
    trade log
    summary

------------------------------------------------
Logs
------------------------------------------------

All logs are written to:
C:/TradingBots/NT/logs/live_log.txt
C:/TradingBots/NT/logs/backtest_log.txt
C:/TradingBots/NT/logs/offline_log.txt

All logs are JSONL-structured, deterministic, and NT-Tech Mode compliant.

------------------------------------------------
End of README
------------------------------------------------
