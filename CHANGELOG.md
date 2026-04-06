# ================================================================
# NT-Tech Changelog (Unified)
# ASCII-only
# ================================================================

------------------------------------------------
## [4.5.4] - MetaStrategy Stable (Current)
------------------------------------------------
- Regime-aware consensus engine
- Volatility Engine (ATR hard gate for entries)
- Volatility-adaptive strategy weights
- Volatility-adaptive open/close thresholds
- EMA-smoothed consensus confidence
- Entry-only anti-whipsaw filtering
- Directional momentum boost
- Compression blocks entries, exits always allowed
- Deterministic behavior preserved
- Logger compatibility with debug tester

------------------------------------------------
## [4.5.x] - MetaStrategy Evolution
------------------------------------------------
- Consensus smoothing introduced
- Anti-whipsaw logic refined
- Entry/exit separation enforced
- Removal of exit blocking conditions
- Progressive stabilization toward 4.5.4

------------------------------------------------
## [4.4]
------------------------------------------------
- Volatility Engine introduced
- ATR-based hard gate
- Volatility-adaptive strategy weights
- Volatility-adaptive thresholds
- Regime-aware normalization

------------------------------------------------
## [3.1] - Strategy Suite Upgrade
------------------------------------------------
- MACDStrategy 3.1 (incremental MACD)
- MACrossoverStrategy 3.1 (incremental EMA/SMA)
- BollingerStrategy 3.1 (incremental SMA + variance)
- RSIStrategy 3.1 (incremental RSI)
- All strategies O(1) per candle
- No ATR or trend filters inside strategies

------------------------------------------------
## [3.0] - Full Engine Upgrade
------------------------------------------------
- ConfigLoader 3.0 with Strict Mode C
- StrategyRouter 3.0 (MetaStrategy as primary)
- BacktestEngine 3.0 (deterministic, long-only)
- LiveEngine 3.0 (Strict Mode C, Binance API)
- FileLogger 3.0 (deterministic, ASCII-only)
- DataLoader 3.0 (deterministic normalization)
- TradeAnalyzer 3.0
- RiskManager deprecated (stub only)
- Utils 3.0 (clamp, round_smart, to_ascii)

------------------------------------------------
## [2.6] - MetaStrategy Incremental Upgrade
------------------------------------------------
- Incremental trend EMA (O(1))
- Incremental ATR (O(1))
- Trend slope filter
- ATR slope filter
- Volatility ratio filter
- Centralized filtering in MetaStrategy
- 2,000,000+ candles/sec performance

------------------------------------------------
## [2.2] - MetaStrategy Baseline
------------------------------------------------
- ATR-based SL/TP
- Trend detection
- Clean signal generation
- Long-only model
- Compatible with BacktestEngine 3.0 and LiveEngine 3.0

------------------------------------------------
End of CHANGELOG
------------------------------------------------
