# ================================================================
# NT-Tech Changelog (Unified)
# ASCII-only
# ================================================================

------------------------------------------------
## [8.4-M] - Modular MetaStrategy + Intrabar Stop Engine (Current Stable)
------------------------------------------------
- Full modular architecture for MetaStrategy (strategy/meta/*)
- Intrabar Stop Engine (synthetic intrabar execution)
    * absolute stop (-6 percent)
    * HWM drawdown stop (-6 percent)
    * ATR trailing stop
    * EMA-ATR stop
    * all stops evaluated using candle.low
- exit_price propagated to OfflineRunner
- OfflineRunner upgraded to 7.6-F (intrabar-aware)
- Eliminated extreme tail losses (worst trade capped at -6 percent)
- Positive average PnL on SOLUSDT-1h (offline diagnostics)
- Deterministic behavior preserved
- Thin wrapper meta_strategy.py maintained for backward compatibility
- Full compatibility with RiskEngine 1.0 and Analyzer 2.1
- Verified compatibility with Night Backtest and LiveEngine dry-run

------------------------------------------------
## [8.3] - MetaStrategy ATR-Adaptive Thresholds
------------------------------------------------
- ATR-adaptive open/close thresholds
- ATR-based dynamic slope and momentum gates
- ATR-normalized breakout logic
- Early version of ATR trailing exit
- Improved stability in high-volatility regimes

------------------------------------------------
## [8.2] - MetaStrategy Two-Stage Engine
------------------------------------------------
- Stage 1 (high recall) + Stage 2 (high precision)
- Confidence smoothing improvements
- Impulse window for momentum/slope/trend
- Regime-aware entry gating
- Reduced false positives in low-volatility environments

------------------------------------------------
## [7.x] - MetaStrategy Evolution (Pre-modular)
------------------------------------------------
- Multiple iterations of entry/exit refinement
- Anti-whipsaw 2.0 stabilization
- Confidence model improvements
- ATR regime filters
- Early HWM tracking
- Non-modular architecture (deprecated)

------------------------------------------------
## [4.7] - MetaStrategy MTF/ATR Upgrade
------------------------------------------------
- Full 1h + 4h MTF architecture
- Internal 4h synthetic candle (4 x 1h)
- ATR Engine 1h + ATR Engine 4h
- ATR regime classification (low / normal / high / extreme)
- Global regime detection (4h)
- MTF bias gate for entries
- Dynamic thresholds 2.0 (regime + ATR)
- Anti-whipsaw 2.0 (entry-only, low-vol enhanced)
- Momentum boost for directional confirmation
- Deterministic consensus normalization
- Fully compatible with PositionManager 2.x and RiskEngine 1.x

------------------------------------------------
## [4.6] - MetaStrategy MTF Foundation
------------------------------------------------
- Introduction of 4h aggregation buffer
- Initial global regime detection
- Initial MTF bias model
- ATR(4h) integration
- Consensus smoothing refinements
- Stabilization of entry/exit hysteresis

------------------------------------------------
## [4.5.4] - MetaStrategy Stable
------------------------------------------------
- Regime-aware consensus engine
- ATR hard gate for entries
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
## [4.4] - Volatility Engine Introduction
------------------------------------------------
- ATR-based hard gate
- Volatility-adaptive strategy weights
- Volatility-adaptive thresholds
- Regime-aware normalization
- First version of volatility-driven consensus shaping

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
