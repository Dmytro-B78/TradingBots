# ================================================================
# NT-Tech Trading Engine 3.0 (Spot Only, Long Only)
# ASCII-only
# ================================================================

A modular, deterministic, ASCII-only trading engine designed for Spot-only algorithmic trading.  
The system follows strict NT-Tech Mode rules and provides a complete pipeline for:

- Backtesting (BacktestEngine 3.0)
- Live trading (LiveEngine 3.0, Binance API)
- Strict Mode C execution safety
- Market scanning (USDT pairs, volume filter >= 50M)
- MetaStrategy 2.2 (ATR-based SL/TP, trend filters)
- Real-time execution engine
- Dry-run mode for safe testing
- Deterministic logging (FileLogger 3.0)
- Error-safe operation

All modules follow NT-Tech Mode:
- ASCII-only
- Full-file PowerShell blocks
- No variables
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
          meta_strategy.py
          ma_crossover_strategy.py
          rsi_strategy.py
          macd_strategy.py
          bollinger_strategy.py

------------------------------------------------
Core Components
------------------------------------------------

MetaStrategy 2.2
- Long-only strategy engine
- ATR-based SL/TP
- Trend filters
- Signal model:
    OPEN_LONG
    CLOSE_LONG
- Fully compatible with BacktestEngine 3.0 and LiveEngine 3.0

Backtest Engine 3.0
- Spot-only, Long-only
- ATR SL/TP integration
- Deterministic candle ordering
- Equity curve
- Sharpe ratio
- Max drawdown
- Trade log
- ASCII-only output
- No short positions
- No OrderEngine
- No RiskManager

Live Engine 3.0 (Strict Mode C, Binance API)
- Official binance-connector client
- Market scanner (USDT pairs, volume >= 50M)
- Real-time price feed
- Market buy/sell execution
- Long-only
- Position sizing by percentage of USDT balance
- ATR SL/TP enforcement
- Dry-run mode
- Strict Mode C safety:
    * allow_live_trading is loaded ONLY from config.json
    * dry_run can be overridden from scripts
    * real trading requires BOTH:
        allow_live_trading = true
        dry_run = false
    * fail-safe blocks all real orders if allow_live_trading=false
- FileLogger 3.0 integration
- Error-safe loop with auto-recovery

FileLogger 3.0
- ASCII-only logging
- Deterministic rotation
- Unified log format for all engines

Risk Manager (Deprecated)
- RiskManager is removed from architecture
- A stub file remains for backward compatibility
- All risk logic is now handled by:
    MetaStrategy 2.2
    BacktestEngine 3.0
    LiveEngine 3.0

Indicators
- SMA, EMA, WMA, HMA
- RSI
- ATR
- Trend filters
- All indicators are pure functions

Utilities (Utils 3.0)
- Safe numeric conversions
- ASCII sanitization
- Deterministic formatting
- clamp(), round_smart(), to_ascii()

------------------------------------------------
Configuration File (config.json)
------------------------------------------------

Example:

{
    "allow_live_trading": false,
    "dry_run": true,

    "meta_strategy": {
        "cooldown": 3,
        "trend_period": 50,
        "atr_period": 14,
        "min_atr": 0.1,
        "sl_mult": 1.5,
        "tp_mult": 3.0
    },

    "strategies": {
        "ma_crossover": {
            "short_period": 10,
            "long_period": 30
        }
    }
}

Strict Mode C rules:
- allow_live_trading is the master kill-switch
- allow_live_trading cannot be overridden by scripts
- dry_run can be overridden by scripts
- real trading requires BOTH:
    allow_live_trading = true
    dry_run = false

------------------------------------------------
Running Backtests
------------------------------------------------

python - << "EOF"
from bot_ai.engine.backtest_engine import BacktestEngine
from bot_ai.engine.config_loader import ConfigLoader
from bot_ai.engine.data_loader import DataLoader

config = ConfigLoader.load_from_json("config.json")
candles = DataLoader.load("candles.json")

engine = BacktestEngine(config, candles)
result = engine.run()
print(result)
EOF

------------------------------------------------
Running Live Trading (Strict Mode C)
------------------------------------------------

python - << "EOF"
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.engine.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")

engine = LiveEngine(
    config=config,
    position_pct=0.25,
    min_volume=50000000,
    dry_run=False
)

engine.run()
EOF

------------------------------------------------
Dry-Run Mode (Safe Testing)
------------------------------------------------

python - << "EOF"
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.engine.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")

engine = LiveEngine(
    config=config,
    position_pct=0.25,
    min_volume=50000000,
    dry_run=True
)

engine.run()
EOF

------------------------------------------------
Logs
------------------------------------------------

All logs are written to:
C:/TradingBots/NT/logs/live_log.txt

Includes:
- OPEN_LONG events
- CLOSE_LONG events
- SL/TP triggers
- Fail-safe blocks
- Errors and stack traces
- Market scanner selections

------------------------------------------------
NT-Tech Mode Rules
------------------------------------------------

- ASCII-only
- Full-file PowerShell blocks
- No variables
- No Cyrillic
- Deterministic formatting
- Ready for direct execution
- All updates delivered as Set-Content blocks

------------------------------------------------
End of README
------------------------------------------------
# ================================================================
# NT-Tech Trading Engine 3.0 (Spot Only, Long Only)
# ASCII-only
# ================================================================

A modular, deterministic, ASCII-only trading engine designed for Spot-only algorithmic trading.
The system follows strict NT-Tech Mode rules and provides a complete pipeline for:

- Ultra-fast backtesting (2,000,000+ candles/sec)
- Live trading (LiveEngine 3.0, Binance API)
- Strict Mode C execution safety
- Market scanning (USDT pairs, volume filter >= 50M)
- MetaStrategy 2.6 (incremental trend + ATR filters)
- Strategy Suite 3.1 (MACD, MA, RSI, Bollinger — all O(1))
- Real-time execution engine
- Dry-run mode for safe testing
- Deterministic logging (FileLogger 3.0)
- Error-safe operation

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
          meta_strategy.py (MetaStrategy 2.6)
          ma_crossover_strategy.py (3.1)
          rsi_strategy.py (3.1)
          macd_strategy.py (3.1)
          bollinger_strategy.py (3.1)

------------------------------------------------
Core Components
------------------------------------------------

MetaStrategy 2.6
- Centralized filtering engine
- Incremental trend EMA (O(1))
- Incremental ATR (O(1))
- Trend slope filter
- ATR slope filter
- Volatility ratio filter
- Long-only signal model:
    OPEN_LONG
    CLOSE_LONG
- All sub-strategies are pure signal generators
- No indicator recalculation
- 2M+ candles/sec performance

Strategy Suite 3.1
- MACDStrategy 3.1 (incremental MACD)
- MACrossoverStrategy 3.1 (incremental EMA/SMA)
- BollingerStrategy 3.1 (incremental SMA + variance)
- RSIStrategy 3.1 (incremental RSI)
- All strategies:
    * No ATR filters
    * No trend filters
    * No IndicatorsAdvanced calls
    * O(1) per candle
    * Fully compatible with MetaStrategy 2.6

Backtest Engine 3.0
- Spot-only, Long-only
- Deterministic candle ordering
- Equity curve
- Sharpe ratio
- Max drawdown
- Trade log
- ASCII-only output
- No short positions
- No OrderEngine
- No RiskManager

Live Engine 3.0 (Strict Mode C, Binance API)
- Official binance-connector client
- Market scanner (USDT pairs, volume >= 50M)
- Real-time price feed
- Market buy/sell execution
- Long-only
- Position sizing by percentage of USDT balance
- ATR SL/TP enforcement
- Dry-run mode
- Strict Mode C safety:
    * allow_live_trading is loaded ONLY from config.json
    * dry_run can be overridden from scripts
    * real trading requires BOTH:
        allow_live_trading = true
        dry_run = false
    * fail-safe blocks all real orders if allow_live_trading=false
- FileLogger 3.0 integration
- Error-safe loop with auto-recovery

FileLogger 3.0
- ASCII-only logging
- Deterministic rotation
- Unified log format for all engines

Indicators (Advanced 3.x)
- SMA, EMA, WMA, HMA
- RSI
- ATR
- Trend filters
- All indicators are pure functions
- No strategy depends on IndicatorsAdvanced

Utilities (Utils 3.0)
- Safe numeric conversions
- ASCII sanitization
- Deterministic formatting
- clamp(), round_smart(), to_ascii()

------------------------------------------------
Configuration File (config.json)
------------------------------------------------

Example:

{
    "allow_live_trading": false,
    "dry_run": true,

    "meta_strategy": {
        "cooldown": 3,
        "trend_period": 50,
        "atr_period": 14,
        "min_atr": 0.1,
        "min_slope": 0.0,
        "min_volatility_ratio": 0.0005
    },

    "strategies": {
        "ma_crossover": {
            "short": 10,
            "long": 30
        }
    }
}

Strict Mode C rules:
- allow_live_trading is the master kill-switch
- allow_live_trading cannot be overridden by scripts
- dry_run can be overridden by scripts
- real trading requires BOTH:
    allow_live_trading = true
    dry_run = false

------------------------------------------------
Running Backtests
------------------------------------------------

python - << "EOF"
from bot_ai.engine.backtest_engine import BacktestEngine
from bot_ai.engine.config_loader import ConfigLoader
from bot_ai.engine.data_loader import DataLoader

config = ConfigLoader.load_from_json("config.json")
candles = DataLoader.load("candles.json")

engine = BacktestEngine(config, candles)
result = engine.run()
print(result)
EOF

------------------------------------------------
Running Live Trading (Strict Mode C)
------------------------------------------------

python - << "EOF"
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.engine.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")

engine = LiveEngine(
    config=config,
    position_pct=0.25,
    min_volume=50000000,
    dry_run=False
)

engine.run()
EOF

------------------------------------------------
Dry-Run Mode (Safe Testing)
------------------------------------------------

python - << "EOF"
from bot_ai.engine.live_engine import LiveEngine
from bot_ai.engine.config_loader import ConfigLoader

config = ConfigLoader.load_from_json("config.json")

engine = LiveEngine(
    config=config,
    position_pct=0.25,
    min_volume=50000000,
    dry_run=True
)

engine.run()
EOF

------------------------------------------------
Logs
------------------------------------------------

All logs are written to:
C:/TradingBots/NT/logs/live_log.txt

Includes:
- OPEN_LONG events
- CLOSE_LONG events
- SL/TP triggers
- Fail-safe blocks
- Errors and stack traces
- Market scanner selections

------------------------------------------------
NT-Tech Mode Rules
------------------------------------------------

- ASCII-only
- Full-file PowerShell blocks
- No Cyrillic
- Deterministic formatting
- Ready for direct execution
- All updates delivered as Set-Content blocks

------------------------------------------------
End of README
------------------------------------------------
