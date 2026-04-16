# ================================================================
# NT-Tech 2026 - LiveEngine 4.3 (Hybrid)
# File: C:\TradingBots\NT\bot_ai\engine\live_engine.py
# ASCII-only, deterministic, no Cyrillic
#
# Modes:
#   - dry-run: historical candles from backtest.candles_path
#   - live: external feed via on_candle(symbol, candle)
#
# Integrations:
#   - SelectorEngine (selector block in config.json)
#   - MetaStrategy 8.4-M (bot_ai.strategy.meta.meta_strategy)
#   - RiskManager (bot_ai.engine.risk_manager)
#   - CSV trade logging
#   - Double safety contour: engine + live blocks in config.json
# ================================================================

import os
import csv
import glob
import time
from datetime import datetime

from bot_ai.strategy.meta.meta_strategy import MetaStrategy
from bot_ai.engine.risk_manager import RiskManager
from bot_ai.selector.selector_engine import SelectorEngine


class LiveEngine:
    """
    Hybrid LiveEngine 4.3:

      - dry-run mode:
          * loads historical candles from backtest.candles_path
          * iterates over allowed_pairs
          * feeds candles into on_candle()

      - live mode:
          * external code calls on_candle(symbol, candle)

      - always:
          * uses SelectorEngine (selector block)
          * uses MetaStrategy 8.4-M
          * uses RiskManager
          * logs all actions to CSV
    """

    def __init__(
        self,
        config=None,
        config_path="C:/TradingBots/NT/config.json",
        log_path="C:/TradingBots/NT/logs/live_trades.csv",
    ):
        self.config_path = config_path
        self.log_path = log_path
        self.config = config or self._load_config()

        # Core config blocks
        self.engine_cfg = self.config.get("engine", {})
        self.live_cfg = self.config.get("live", {})
        self.bt_cfg = self.config.get("backtest", {})
        self.sel_cfg = self.config.get("selector", {})
        self.risk_cfg = self.config.get("risk", {})
        self.strategy_cfg = self.config.get("strategy", {})

        # Paths and timeframe
        self.candles_path = self.bt_cfg.get("candles_path", "candles")
        self.timeframe = self.bt_cfg.get("timeframe", "1h")

        # Selector
        self.selector_reload_sec = int(self.sel_cfg.get("reload_sec", 60))
        self._last_reload_ts = 0
        self.selector = SelectorEngine(self.sel_cfg) if self.sel_cfg else None
        self.allowed_pairs = set()

        # Strategy + Risk
        strat_params = self.strategy_cfg.get("params", {})
        self.meta = MetaStrategy(strat_params)
        self.risk = RiskManager(self.risk_cfg)

        self.last_action = None

        # Logging
        self._init_log()
        self._log("LiveEngine 4.3 (Hybrid) initialized.")
        self._log_safety_summary()

        # Initial allowed_pairs load
        self._reload_allowed_pairs(force=True)

    # ------------------------------------------------------------
    # Config loader
    # ------------------------------------------------------------
    def _load_config(self):
        try:
            with open(self.config_path, "r", encoding="ascii", errors="ignore") as f:
                import json

                return json.load(f)
        except Exception:
            print("[LiveEngine] ERROR: cannot load config.json")
            return {}

    # ------------------------------------------------------------
    # Safety summary
    # ------------------------------------------------------------
    def _log_safety_summary(self):
        eng = self.engine_cfg
        live = self.live_cfg

        self._log(
            "Safety(engine): allow_live_trading="
            + str(eng.get("allow_live_trading", False))
            + ", dry_run="
            + str(eng.get("dry_run", True))
        )
        self._log(
            "Safety(live): dry_run="
            + str(live.get("dry_run", True))
            + ", api_enabled="
            + str(live.get("api_enabled", False))
            + ", allow_live_trading="
            + str(live.get("allow_live_trading", False))
            + ", require_manual_confirm="
            + str(live.get("require_manual_confirm", True))
        )

    # ------------------------------------------------------------
    # Logging helpers
    # ------------------------------------------------------------
    def _init_log(self):
        log_dir = os.path.dirname(self.log_path)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(
                    [
                        "timestamp",
                        "symbol",
                        "open",
                        "high",
                        "low",
                        "close",
                        "meta_signal",
                        "risk_action",
                        "position",
                        "atr_1h",
                        "atr_4h",
                        "local_regime",
                        "global_regime",
                        "mtf_bias_4h",
                    ]
                )

    def _log(self, msg):
        ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] {msg}"
        print(line)
        try:
            with open(self.log_path, "a", encoding="ascii", errors="ignore") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def _log_trade(self, symbol, candle, meta_signal, risk_action, meta_state, position):
        ts = int(time.time())
        with open(self.log_path, "a", newline="") as f:
            w = csv.writer(f)
            w.writerow(
                [
                    ts,
                    symbol,
                    candle.get("open"),
                    candle.get("high"),
                    candle.get("low"),
                    candle.get("close"),
                    meta_signal,
                    risk_action,
                    position,
                    meta_state.get("atr_1h"),
                    meta_state.get("atr_4h"),
                    meta_state.get("local_regime"),
                    meta_state.get("global_regime"),
                    meta_state.get("mtf_bias_4h"),
                ]
            )

    # ------------------------------------------------------------
    # Selector / allowed_pairs
    # ------------------------------------------------------------
    def _reload_allowed_pairs(self, force=False):
        now = time.time()
        if not force and (now - self._last_reload_ts < self.selector_reload_sec):
            return

        self._last_reload_ts = now

        pairs = []
        if self.selector is not None:
            try:
                pairs = self.selector.get_top_pairs()
            except Exception as e:
                self._log(f"SelectorEngine error: {e}")

        if not pairs:
            all_pairs = self.sel_cfg.get("all_pairs", [])
            pairs = list(all_pairs)

        new_set = set(pairs)
        if new_set != self.allowed_pairs:
            self.allowed_pairs = new_set
            self._log(f"[LiveEngine] allowed_pairs updated: {self.allowed_pairs}")

    # ------------------------------------------------------------
    # Candle loading for dry-run
    # ------------------------------------------------------------
    def _load_candles_for_symbol(self, symbol):
        base = self.candles_path
        tf = self.timeframe

        pattern = os.path.join(base, f"{symbol}-{tf}-*.csv")
        files = sorted(glob.glob(pattern))
        if not files:
            self._log(f"No candle files for {symbol} with pattern {pattern}")
            return []

        path = files[-1]
        self._log(f"Loading candles for {symbol} from {path}")

        candles = []
        try:
            with open(path, "r", encoding="ascii", errors="ignore") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) < 6:
                        continue
                    candles.append(
                        {
                            "open": float(row[1]),
                            "high": float(row[2]),
                            "low": float(row[3]),
                            "close": float(row[4]),
                            "volume": float(row[5]),
                        }
                    )
        except Exception as e:
            self._log(f"Error loading candles for {symbol}: {e}")
            return []

        self._log(f"Loaded {len(candles)} candles for {symbol}")
        return candles

    # ------------------------------------------------------------
    # Core processing
    # ------------------------------------------------------------
    def _build_meta_state_for_risk(self, state):
        return {
            "atr_1h": state.get("atr_1h"),
            "atr_4h": state.get("atr_4h"),
            "atr_regime_1h": state.get("atr_regime_1h"),
            "atr_regime_4h": state.get("atr_regime_4h"),
            "local_regime": state.get("local_regime"),
            "global_regime": state.get("global_regime"),
            "mtf_bias_4h": state.get("mtf_bias_4h"),
        }

    def _process_candle_internal(self, symbol, candle, is_dry):
        # MetaStrategy step (new API)
        state = self.meta.compute_meta_state(candle)
        decision = self.meta.compute_meta_signal(state)

        # FIX: pass full decision object to RiskManager, not just string
        meta_signal = decision

        meta_state_for_risk = self._build_meta_state_for_risk(state)

        # RiskManager step
        risk_action = self.risk.on_candle(
            candle=candle,
            meta_signal=meta_signal,
            meta_state=meta_state_for_risk,
        )

        # Sync position
        self.meta.position = self.risk.position

        result = {
            "symbol": symbol,
            "candle": candle,
            "meta_signal": meta_signal,
            "meta_state": meta_state_for_risk,
            "risk_action": risk_action,
            "position": self.risk.position,
        }

        self.last_action = result

        # Log trade
        self._log_trade(
            symbol=symbol,
            candle=candle,
            meta_signal=meta_signal,
            risk_action=risk_action,
            meta_state=meta_state_for_risk,
            position=self.risk.position,
        )

        return result

    # ------------------------------------------------------------
    # Public candle handler (live mode)
    # ------------------------------------------------------------
    def on_candle(self, symbol, candle):
        """
        Live mode handler.
        External feed calls this method with new candles.
        Selector integration:
          - auto-reload allowed_pairs
          - skip symbols not in allowed_pairs (if non-empty)
        """
        self._reload_allowed_pairs(force=False)

        if self.allowed_pairs and symbol not in self.allowed_pairs:
            return None

        return self._process_candle_internal(symbol, candle, is_dry=False)

    # ------------------------------------------------------------
    # Dry-run mode (historical)
    # ------------------------------------------------------------
    def _run_dry(self):
        self._log("Starting LiveEngine dry-run (historical mode).")

        self._reload_allowed_pairs(force=True)
        if not self.allowed_pairs:
            self._log("No allowed_pairs in dry-run. Exiting.")
            return

        total_candles = 0
        for symbol in sorted(self.allowed_pairs):
            candles = self._load_candles_for_symbol(symbol)
            total_candles += len(candles)
            for c in candles:
                self._process_candle_internal(symbol, c, is_dry=True)

        self._log(f"Dry-run completed. Total candles processed: {total_candles}")

    # ------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------
    def reset(self):
        strat_params = self.strategy_cfg.get("params", {})
        self.meta = MetaStrategy(strat_params)
        self.risk = RiskManager(self.risk_cfg)
        self.last_action = None

    # ------------------------------------------------------------
    # Entry point
    # ------------------------------------------------------------
    def start(self):
        dry = bool(self.live_cfg.get("dry_run", True))
        if dry:
            self._run_dry()
        else:
            self._log("Live mode started. Waiting for external on_candle() feed.")
