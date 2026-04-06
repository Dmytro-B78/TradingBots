# ================================================================
# File: bot_ai/strategy/meta_strategy.py
# NT-Tech MetaStrategy 4.5.4 (Variant 1)
# - Compression blocks entries only
# - Exits are always allowed (no force-close)
# - Keeps 4.4 Volatility Engine + 4.5 entry-only anti-whipsaw
# - Logger strategy_signals preserved for debug
# ASCII-only, deterministic, no Cyrillic
# ================================================================

from bot_ai.engine.signal_logger import SignalLogger
from bot_ai.strategy.ma_crossover_strategy import MACrossoverStrategy
from bot_ai.strategy.macd_strategy import MACDStrategy
from bot_ai.strategy.rsi_strategy import RSIStrategy
from bot_ai.strategy.bollinger_strategy import BollingerStrategy
from bot_ai.strategy.microtrend_strategy import MicroTrendStrategy


class MetaStrategy:
    def __init__(self, config=None):
        config = config or {}

        # Base thresholds
        self.open_threshold = float(config.get("open_threshold", 0.5))
        self.close_threshold = float(config.get("close_threshold", -0.5))

        # Hysteresis
        self.open_hysteresis = int(config.get("open_hysteresis", 2))
        self.close_hysteresis = int(config.get("close_hysteresis", 2))
        self.open_lock = 0
        self.close_lock = 0

        self.position = None
        self.regime = "range"

        # Volatility engine (ATR)
        self.atr_period = int(config.get("atr_period", 14))
        self.atr_min_pct = float(config.get("atr_min_pct", 0.0010))
        self.atr_max_pct = float(config.get("atr_max_pct", 0.0200))
        self.vol_thr_low_mult = float(config.get("vol_thr_low_mult", 0.85))
        self.vol_thr_high_mult = float(config.get("vol_thr_high_mult", 1.25))
        self.vol_weight_low_boost = float(config.get("vol_weight_low_boost", 1.15))
        self.vol_weight_high_boost = float(config.get("vol_weight_high_boost", 1.15))
        self.vol_weight_penalty = float(config.get("vol_weight_penalty", 0.85))

        # Consensus smoothing (entry-only anti-whipsaw)
        self.ema_alpha = float(config.get("ema_alpha", 0.50))
        self.momentum_boost = float(config.get("momentum_boost", 0.12))
        self.whipsaw_delta = float(config.get("whipsaw_delta", 0.30))
        self.prev_ema_conf = None
        self.ema_conf = None

        # Weights
        self.weights = {
            "MACrossoverStrategy": 1.5,
            "MACDStrategy": 2.0,
            "RSIStrategy": 1.5,
            "BollingerStrategy": 2.0,
            "MicroTrendStrategy": 1.0
        }

        # Regime strategies
        self.regime_strategies = {
            "trend": ["MACrossoverStrategy", "MACDStrategy", "MicroTrendStrategy"],
            "range": ["RSIStrategy", "BollingerStrategy"],
            "expansion": ["MACrossoverStrategy", "MACDStrategy", "BollingerStrategy"],
            "compression": []  # entries blocked; exits allowed
        }

        self.strategies = [
            MACrossoverStrategy(),
            MACDStrategy(),
            RSIStrategy(),
            BollingerStrategy(),
            MicroTrendStrategy()
        ]

        self.recent_candles = []
        self.logger = SignalLogger()

    # ------------------------------------------------------------
    # Regime detection
    # ------------------------------------------------------------
    def detect_regime(self, candle):
        o = candle["open"]
        h = candle["high"]
        l = candle["low"]
        c = candle["close"]

        body = abs(c - o)
        rng = h - l

        if rng <= 0:
            return "compression"

        body_ratio = body / rng

        if body_ratio >= 0.65:
            return "trend"
        if body_ratio <= 0.18:
            return "compression"
        if 0.18 < body_ratio < 0.65 and rng > abs(c) * 0.01:
            return "expansion"

        return "range"

    # ------------------------------------------------------------
    # ATR helpers
    # ------------------------------------------------------------
    def compute_atr(self):
        if len(self.recent_candles) < (self.atr_period + 1):
            return None

        trs = []
        start = len(self.recent_candles) - (self.atr_period + 1)
        prev_close = self.recent_candles[start]["close"]

        for i in range(start + 1, len(self.recent_candles)):
            c = self.recent_candles[i]
            h = c["high"]
            l = c["low"]
            tr = max(h - l, abs(h - prev_close), abs(l - prev_close))
            trs.append(tr)
            prev_close = c["close"]

        return sum(trs) / float(len(trs)) if trs else None

    def compute_atr_pct(self, candle):
        atr = self.compute_atr()
        if atr is None or candle["close"] <= 0:
            return None
        return atr / candle["close"]

    def get_vol_state(self, atr_pct):
        if atr_pct is None:
            return None
        mid = (self.atr_min_pct + self.atr_max_pct) / 2.0
        return "high" if atr_pct >= mid else "low"

    def get_vol_threshold_multiplier(self, atr_pct):
        if atr_pct is None:
            return 1.0
        if atr_pct <= self.atr_min_pct:
            return self.vol_thr_low_mult
        if atr_pct >= self.atr_max_pct:
            return self.vol_thr_high_mult
        span = self.atr_max_pct - self.atr_min_pct
        t = (atr_pct - self.atr_min_pct) / span if span > 0 else 0.0
        return self.vol_thr_low_mult + t * (self.vol_thr_high_mult - self.vol_thr_low_mult)

    def get_vol_weight_multiplier(self, name, atr_pct):
        state = self.get_vol_state(atr_pct)
        if state is None:
            return 1.0
        if state == "high":
            if name in ["MACrossoverStrategy", "MACDStrategy"]:
                return self.vol_weight_high_boost
            if name in ["RSIStrategy", "BollingerStrategy"]:
                return self.vol_weight_penalty
            return 1.0
        if name in ["RSIStrategy", "BollingerStrategy"]:
            return self.vol_weight_low_boost
        if name in ["MACrossoverStrategy", "MACDStrategy"]:
            return self.vol_weight_penalty
        return 1.0

    # ------------------------------------------------------------
    # Dynamic thresholds by regime
    # ------------------------------------------------------------
    def get_dynamic_thresholds(self):
        open_thr = self.open_threshold
        close_thr = self.close_threshold
        if self.regime == "trend":
            open_thr -= 0.15
            close_thr += 0.15
        elif self.regime == "range":
            open_thr += 0.10
            close_thr -= 0.10
        elif self.regime == "expansion":
            open_thr -= 0.05
        return (
            max(min(open_thr, 1.0), -1.0),
            max(min(close_thr, 1.0), -1.0),
        )

    # ------------------------------------------------------------
    # Max possible confidence for current regime
    # ------------------------------------------------------------
    def get_regime_max_conf(self, allowed, atr_pct):
        if not allowed:
            return 1.0
        total = 0.0
        for name in allowed:
            w = self.weights.get(name, 1.0)
            w *= self.get_vol_weight_multiplier(name, atr_pct)
            if self.regime == "trend":
                w *= 1.25
            elif self.regime == "expansion":
                w *= 0.9
            total += w
        return max(total, 1.0)

    # ------------------------------------------------------------
    # Main candle handler
    # ------------------------------------------------------------
    def on_candle(self, candle, position):
        self.position = position
        self.regime = self.detect_regime(candle)

        if self.open_lock > 0:
            self.open_lock -= 1
        if self.close_lock > 0:
            self.close_lock -= 1

        self.recent_candles.append(candle)
        if len(self.recent_candles) > 200:
            self.recent_candles.pop(0)

        allowed = self.regime_strategies.get(self.regime, None)
        atr_pct = self.compute_atr_pct(candle)

        # Compression: block entries only (no early return)
        entries_blocked = (allowed == [])

        # ATR hard gate: entries only
        if self.position is None and atr_pct is not None:
            if atr_pct < self.atr_min_pct or atr_pct > self.atr_max_pct:
                self.logger.log(candle, self.regime, 0.0, None, [])
                self.logger.last_decision = None
                return None

        strategy_signals = []
        total_conf = 0.0

        for strat in self.strategies:
            name = strat.__class__.__name__
            if allowed is not None and name not in allowed:
                continue
            if hasattr(strat, "set_regime"):
                strat.set_regime(self.regime)
            sig = strat.on_candle(candle)
            conf = 1.0 if sig == "BUY" else -1.0 if sig == "SELL" else 0.0
            w = self.weights.get(name, 1.0)
            w *= self.get_vol_weight_multiplier(name, atr_pct)
            weighted = conf * w
            if self.regime == "trend":
                weighted *= 1.25
            elif self.regime == "expansion":
                weighted *= 0.9
            strategy_signals.append((name, sig, weighted))
            total_conf += weighted

        max_conf = self.get_regime_max_conf(allowed, atr_pct)
        norm_conf = total_conf / max_conf
        norm_conf = max(min(norm_conf, 1.0), -1.0)

        # EMA smoothing
        if self.ema_conf is None:
            self.ema_conf = norm_conf
        else:
            self.ema_conf = self.ema_alpha * norm_conf + (1.0 - self.ema_alpha) * self.ema_conf

        delta = 0.0
        if self.prev_ema_conf is not None:
            delta = self.ema_conf - self.prev_ema_conf

        # Entry-only anti-whipsaw + aligned momentum
        if self.position is None and not entries_blocked:
            if abs(delta) >= self.whipsaw_delta:
                self.prev_ema_conf = self.ema_conf
                self.logger.log(candle, self.regime, total_conf, None, strategy_signals)
                self.logger.last_decision = None
                return None
            if delta * self.ema_conf > 0:
                self.ema_conf += delta * self.momentum_boost

        self.prev_ema_conf = self.ema_conf
        smooth_conf = max(min(self.ema_conf, 1.0), -1.0)

        # Log for debug
        self.logger.log(candle, self.regime, total_conf, None, strategy_signals)

        open_thr, close_thr = self.get_dynamic_thresholds()
        thr_mult = self.get_vol_threshold_multiplier(atr_pct)
        open_thr *= thr_mult
        close_thr *= thr_mult
        open_thr = max(min(open_thr, 1.0), -1.0)
        close_thr = max(min(close_thr, 1.0), -1.0)

        # Entries blocked in compression
        if self.position is None and not entries_blocked:
            if smooth_conf >= open_thr and self.open_lock == 0:
                self.open_lock = self.open_hysteresis
                decision = {"signal": "OPEN_LONG", "confidence": smooth_conf, "regime": self.regime}
                self.logger.last_decision = decision
                return decision

        # Exits always allowed
        if self.position == "LONG":
            if smooth_conf <= close_thr and self.close_lock == 0:
                self.close_lock = self.close_hysteresis
                decision = {"signal": "CLOSE_LONG", "confidence": smooth_conf, "regime": self.regime}
                self.logger.last_decision = decision
                return decision

        self.logger.last_decision = None
        return None
