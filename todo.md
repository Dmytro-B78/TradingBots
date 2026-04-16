# ================================================================
# NT-Tech Mode - TODO Roadmap
# Checkpoint: NT_SNAPSHOT_2026-04-16_META_8_4_M_OK
# ASCII-only
# ================================================================

Project is in a stable state:
- MetaStrategy 8.4-M (modular, ATR-aware, intrabar stops)
- OfflineRunner 7.6-F (intrabar-aware exit_price)
- Analyzer 2.1 fully compatible
- Logs are compact and reproducible
- Pipeline is stable and deterministic

All further actions are executed strictly by stages.

================================================
# STAGE 1 - Strategy diagnostics (COMPLETED)
================================================

## 1.1. Distribution analysis
- [x] PnL distribution by duration_bars
- [x] PnL distribution by atr_1h_entry
- [x] PnL distribution by regime / global_regime
- [x] PnL distribution by confidence_entry
- [x] Extract toxic zones and strong zones

## 1.2. Heatmaps
- [x] ATR x Regime -> average PnL
- [x] Confidence x Regime -> average PnL
- [x] Duration x PnL
- [x] Extract toxic and strong zones

## 1.3. Toxic zone detection
- [x] ATR zones with negative expectation
- [x] Regime phases with negative expectation
- [x] Confidence levels without edge
- [x] Duration patterns leading to losses

## 1.4. Report formation
- [x] Strong zones (edge)
- [x] Weak zones (toxic)
- [x] Recommendations for MetaStrategy
- [x] Recommendations for RiskGuard
- [x] diagnostics/strategy_diagnostics_report.md

================================================
# STAGE 2 - MetaStrategy improvements (IN PROGRESS)
================================================

## 2.1. Filters (COMPLETED)
- [x] ATR filter (exclude low-vol zones)
- [x] Regime filter (exclude range phases)
- [x] Confidence filter (exclude weak signals)

## 2.2. Signal improvements (PARTIAL)
- [x] Momentum component integrated
- [x] Volatility-aware logic integrated
- [ ] Additional smoothing of meta_signal
- [ ] Add 2-bar confirmation for exit conditions
- [ ] Add confidence hysteresis

## 2.3. Global regime improvements (PENDING)
- [ ] Reduce noise in global regime
- [ ] Add hysteresis
- [ ] Add memory buffer (EMA-based)
- [ ] Improve expansion detection

================================================
# STAGE 3 - RiskGuard improvements (NEXT)
================================================

## 3.1. Adaptive sizing
- [ ] Position size depends on ATR
- [ ] Position size depends on confidence
- [ ] Position size depends on regime
- [ ] Add exposure cap per pair

## 3.2. Adaptive stop logic
- [ ] Stop depends on ATR regime
- [ ] Stop depends on local/global regime
- [ ] Stop depends on duration
- [ ] Add volatility shock override

## 3.3. Kill-switch
- [ ] Losing streak -> pause
- [ ] Daily/weekly risk limits
- [ ] Global kill-switch

================================================
# STAGE 4 - Analyzer 2.2 (optional)
================================================

## 4.1. Duration histogram (bars)
- [ ] Switch Analyzer to duration_bars

## 4.2. Interface improvements
- [ ] Colored ASCII histograms
- [ ] Summary-only mode
- [ ] Two-log comparison (A/B test)
- [ ] Anomaly trade detection
- [ ] Regime-phase breakdown

================================================
# STAGE 5 - Real-time readiness
================================================

## 5.1. Real-time runner
- [ ] Streaming candles
- [ ] Streaming meta_signal computation
- [ ] Streaming RiskGuard
- [ ] Real-time intrabar stop simulation

## 5.2. Real-time logging
- [ ] Minimal log
- [ ] Separate error log
- [ ] Separate trades log
- [ ] Structured JSON mode

## 5.3. Real-time alerts
- [ ] Telegram / Discord notifications
- [ ] Anomalies / errors / signals
- [ ] Kill-switch alerts

================================================
# STAGE 6 - Final stabilization
================================================

## 6.1. Regression tests
- [ ] MetaStrategy tests
- [ ] RiskGuard tests
- [ ] Runner tests
- [ ] Analyzer tests
- [ ] OfflineRunner tests

## 6.2. Final snapshot
- [ ] NT_SNAPSHOT_YYYY-MM-DD_FINAL

================================================
End of TODO
================================================
