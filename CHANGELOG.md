# ================================================================
# NT-Tech Changelog (Unified)
# Versions: BacktestEngine 3.0, LiveEngine 3.0, MetaStrategy 2.2
# ASCII-only
# ================================================================

## [3.0] - Full Engine Upgrade
### Major Architecture Changes
- Introduced ConfigLoader 3.0 with support for:
  - allow_live_trading (Strict Mode C)
  - dry_run override
  - meta_strategy block
  - strategy parameter blocks
- Removed legacy fields: strategy, params, risk, engine.
- StrategyRouter upgraded to 3.0:
  - MetaStrategy is now the primary strategy.
  - All strategies loaded from config["strategies"].
  - Removed RiskManager dependency.

### Backtest Engine 3.0
- Fully rewritten for MetaStrategy 2.2.
- Deterministic candle ordering.
- Clean equity curve computation.
- Stable metrics (Sharpe, drawdown, winrate).
- ASCII-only output.
- No short positions, no OrderEngine, no RiskManager.

### Live Engine 3.0
- Strict Mode C enforcement:
  - Real trading allowed ONLY if:
    allow_live_trading = true AND dry_run = false.
- Integrated FileLogger 3.0.
- Deterministic logging.
- Clean SL/TP execution from MetaStrategy.
- Market scanner rewritten.
- ASCII-only.

### FileLogger 3.0
- ASCII-only logging.
- Deterministic rotation.
- Unified log format across all engines.

### DataLoader 3.0
- Deterministic JSON/CSV loader.
- Strict Binance-style normalization.
- ASCII-only.
- Guaranteed unique open_time.

### TradeAnalyzer 3.0
- Deterministic trade ordering.
- Stable metrics.
- ASCII-only.

### RiskManager Deprecated
- Fully removed from architecture.
- Replaced with a stub for backward compatibility.
- All risk logic now handled by:
  - MetaStrategy 2.2
  - BacktestEngine 3.0
  - LiveEngine 3.0

### Utils 3.0
- ASCII-only sanitization.
- Deterministic conversions.
- Added clamp(), round_smart(), to_ascii().

### MetaStrategy 2.2
- ATR-based SL/TP.
- Trend detection.
- Clean signal generation.
- Fully compatible with BacktestEngine 3.0 and LiveEngine 3.0.
# ================================================================
# NT-Tech Changelog (Unified)
# Versions: BacktestEngine 3.0, LiveEngine 3.0, MetaStrategy 2.6
# ASCII-only
# ================================================================

## [3.0] - Full Engine Upgrade
### Major Architecture Changes
- Introduced ConfigLoader 3.0 with support for:
  - allow_live_trading (Strict Mode C)
  - dry_run override
  - meta_strategy block
  - strategy parameter blocks
- Removed legacy fields: strategy, params, risk, engine.
- StrategyRouter upgraded to 3.0:
  - MetaStrategy is now the primary strategy.
  - All strategies loaded from config["strategies"].
  - Removed RiskManager dependency.

### Backtest Engine 3.0
- Fully rewritten for MetaStrategy 2.6.
- Deterministic candle ordering.
- Clean equity curve computation.
- Stable metrics (Sharpe, drawdown, winrate).
- ASCII-only output.
- No short positions, no OrderEngine, no RiskManager.

### Live Engine 3.0
- Strict Mode C enforcement:
  - Real trading allowed ONLY if:
    allow_live_trading = true AND dry_run = false.
- Integrated FileLogger 3.0.
- Deterministic logging.
- Clean SL/TP execution from MetaStrategy.
- Market scanner rewritten.
- ASCII-only.

### FileLogger 3.0
- ASCII-only logging.
- Deterministic rotation.
- Unified log format across all engines.

### DataLoader 3.0
- Deterministic JSON/CSV loader.
- Strict Binance-style normalization.
- ASCII-only.
- Guaranteed unique open_time.

### TradeAnalyzer 3.0
- Deterministic trade ordering.
- Stable metrics.
- ASCII-only.

### RiskManager Deprecated
- Fully removed from architecture.
- Replaced with a stub for backward compatibility.
- All risk logic now handled by:
  - MetaStrategy 2.6
  - BacktestEngine 3.0
  - LiveEngine 3.0

### Utils 3.0
- ASCII-only sanitization.
- Deterministic conversions.
- Added clamp(), round_smart(), to_ascii().

------------------------------------------------
## [2.6] - MetaStrategy Incremental Upgrade
### Incremental Filters (O(1))
- Added incremental trend EMA (no history scans).
- Added incremental ATR (no history scans).
- Added trend slope filter.
- Added ATR slope filter.
- Added volatility ratio filter.
- Removed all IndicatorsAdvanced calls from strategies.
- Centralized all filtering logic inside MetaStrategy.

### Performance
- Achieved 2,000,000+ candles/sec on real datasets.
- Zero performance degradation over time.
- Fully deterministic execution.

------------------------------------------------
## [3.1] - Strategy Suite Upgrade
### MACDStrategy 3.1
- Incremental MACD (fast, slow, signal).
- Removed ATR filter.
- Removed trend filter.
- O(1) per candle.

### MACrossoverStrategy 3.1
- Incremental EMA/SMA.
- Removed ATR filter.
- Removed trend filter.
- O(1) per candle.

### BollingerStrategy 3.1
- Incremental SMA + variance (Welford).
- Removed ATR filter.
- Removed trend filter.
- O(1) per candle.

### RSIStrategy 3.1
- Incremental RSI (Wilder).
- Removed ATR filter.
- Removed trend filter.
- O(1) per candle.

------------------------------------------------
## [3.0] - IndicatorsAdvanced Cleanup
- IndicatorsAdvanced no longer used by strategies.
- All strategies fully incremental.
- Indicators remain available for external tools.

------------------------------------------------
End of CHANGELOG
------------------------------------------------
