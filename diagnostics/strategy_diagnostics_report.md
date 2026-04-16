# Strategy Diagnostics Report
# Source: logs/offline_log.txt
# Scope: Stage 1 (Distribution, Heatmaps, Toxic zones)

---

## 1. Strong zones (edge)

### 1.1. ATR strong zones

- 1.0 - 1.5
- 2.0 - 3.0
- 3.5 - 4.0  (best)

### 1.2. Confidence strong zones

- 0.05 - 0.30
- 0.45 - 0.55

### 1.3. Duration strong zones

- 80 - 255 bars

### 1.4. Regime strong zones

- trend (only regime present in current data)
- regime model is not discriminative yet

---

## 2. Toxic zones (negative expectation)

### 2.1. ATR toxic zones

- 1.5 - 2.0
- 4.5 - 6.0
- > 7.0

### 2.2. Confidence toxic zones

- 0.40 - 0.45
- 0.55 - 0.65

### 2.3. Duration toxic zones

- 0 - 20 bars
- 35 - 50 bars
- 60 - 75 bars

### 2.4. Regime toxic zones

- none detected (all trades in trend)
- main issue: regime model does not separate regimes

---

## 3. MetaStrategy recommendations

### 3.1. ATR-based filters

- Prefer trades when ATR_1h_entry is in:
  - 1.0 - 1.5
  - 2.0 - 3.0
  - 3.5 - 4.0
- Avoid or downweight trades when ATR_1h_entry is in:
  - 1.5 - 2.0
  - 4.5 - 6.0
  - > 7.0

### 3.2. Confidence-based filters

- Prefer trades when confidence_entry is in:
  - 0.05 - 0.30
  - 0.45 - 0.55
- Avoid or downweight trades when confidence_entry is in:
  - 0.40 - 0.45
  - 0.55 - 0.65
- Consider hard cutoff:
  - ignore confidence_entry < 0.05 (no edge)
  - ignore confidence_entry > 0.65 (too unstable, low sample size)

### 3.3. Duration-aware logic

- MetaStrategy should be designed to hold positions longer:
  - target holding: 80+ bars when conditions remain valid
- Avoid patterns that systematically close trades:
  - before 20 bars without strong adverse move
  - in 35 - 50 and 60 - 75 bar ranges without clear reason

### 3.4. Regime model

- Current local_regime_entry is almost always "trend"
- Action items:
  - improve regime detection to separate:
    - trend up
    - trend down
    - range
    - high volatility chop
  - use regime as an additional filter only after it becomes discriminative

---

## 4. RiskGuard recommendations

### 4.1. ATR-aware sizing

- Increase position size in strong ATR zones:
  - 1.0 - 1.5
  - 2.0 - 3.0
  - 3.5 - 4.0
- Decrease or zero position size in toxic ATR zones:
  - 1.5 - 2.0
  - 4.5 - 6.0
  - > 7.0

### 4.2. Confidence-aware sizing

- Scale position size with confidence_entry inside strong zones:
  - 0.05 - 0.30
  - 0.45 - 0.55
- Cap or reduce size in:
  - 0.40 - 0.45
  - 0.55 - 0.65

### 4.3. Duration-aware stops

- Avoid forced exits before 20 bars unless:
  - hard stop is hit
  - regime changes to clearly adverse
- Allow extended holding (80+ bars) when:
  - ATR remains in strong zones
  - confidence does not collapse
  - no regime flip to clearly adverse state

### 4.4. Kill-switch design

- Use streak-based kill-switch:
  - N consecutive losing trades in toxic zones -> pause trading
- Use daily/weekly loss limits:
  - if cumulative PnL < threshold -> pause trading
- Log all kill-switch events for further diagnostics

---

## 5. Summary

- Strategy has clear edge in:
  - specific ATR ranges
  - specific confidence ranges
  - long holding durations (80+ bars)
- Strategy systematically loses in:
  - short holding durations
  - high ATR extremes
  - specific confidence bands
- Next stages (2 and 3) should:
  - implement filters based on these zones
  - adjust sizing and stops accordingly
  - improve regime model to become a real filter
