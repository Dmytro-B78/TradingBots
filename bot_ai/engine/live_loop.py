# ================================================================
# File: bot_ai/engine/live_loop.py
# NT-Tech Hybrid Live Loop (REST core, WS-ready scaffold)
# - Symbol: SOLUSDT
# - Interval: 1h
# - Equity refresh: 10 seconds
# ASCII-only
# ================================================================

import time
import json
from typing import Optional, Dict, Any

import requests

from bot_ai.engine.config_loader import ConfigLoader
from bot_ai.engine.file_logger import FileLogger
from bot_ai.engine.live_engine import LiveEngine

from bot_ai.execution.execution_manager import ExecutionManager
from bot_ai.execution.execution_router import ExecutionRouter


class LiveLoop:
    """
    NT-Tech Hybrid Live Loop.

    Deterministic flow:
      - REST polling for latest kline
      - Feed candle into LiveEngine.on_candle(...)
      - Map risk_action -> execution decision
      - SAFETY GUARDS (allow_live_trading / dry_run)
      - Execute via ExecutionRouter (lazy-initialized)
    """

    def __init__(
        self,
        symbol: str = "SOLUSDT",
        interval: str = "1h",
        equity_refresh_seconds: int = 10,
        config_path: str = "config.json",
    ) -> None:
        self.symbol = symbol.upper()
        self.interval = interval
        self.equity_refresh_seconds = int(equity_refresh_seconds)
        self.config_path = config_path

        self.last_kline_close_time_ms: Optional[int] = None

        self.session = requests.Session()

        self.config = self._load_config(self.config_path)

        binance_cfg = self.config.get("binance", {})
        self.rest_base_url = binance_cfg.get("rest_base_url", "https://api.binance.com")

        live_cfg = self.config.get("live_engine", {})
        self.engine = LiveEngine(live_cfg)

        self.allow_live = bool(self.config.get("allow_live_trading", False))
        self.dry_run = bool(self.config.get("dry_run", False))

        self.exec_router: Optional[ExecutionRouter] = None
        if self.allow_live:
            self.exec_router = self._build_execution_router(self.config)
        else:
            FileLogger.info("Execution stack disabled (allow_live_trading = false)")

        FileLogger.info(
            f"LiveLoop initialized: symbol={self.symbol}, interval={self.interval}, "
            f"allow_live_trading={self.allow_live}, dry_run={self.dry_run}"
        )

    # ------------------------------------------------------------
    # Config
    # ------------------------------------------------------------
    def _load_config(self, path: str) -> Dict[str, Any]:
        cfg = ConfigLoader.load_from_json(path)
        FileLogger.info("LiveLoop config loaded successfully")
        return cfg

    def _build_execution_router(self, config: Dict[str, Any]) -> ExecutionRouter:
        ex_cfg = config.get("exchange", {})
        api_key = ex_cfg.get("api_key")
        api_secret = ex_cfg.get("api_secret")
        base_url = ex_cfg.get("base_url", "https://api.binance.com")

        if not api_key or not api_secret:
            raise Exception("Missing exchange.api_key or exchange.api_secret in config.json")

        manager = ExecutionManager(api_key, api_secret, base_url)
        router = ExecutionRouter(manager)

        FileLogger.info("Execution stack initialized")
        return router

    # ------------------------------------------------------------
    # Binance REST helpers
    # ------------------------------------------------------------
    def _get_latest_kline(self) -> Optional[Dict[str, Any]]:
        url = f"{self.rest_base_url}/api/v3/klines"
        params = {"symbol": self.symbol, "interval": self.interval, "limit": 1}

        try:
            resp = self.session.get(url, params=params, timeout=5)
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            FileLogger.error(f"Error fetching kline for {self.symbol}: {e}")
            return None

        if not data or not isinstance(data, list):
            FileLogger.error(f"Invalid kline response for {self.symbol}: {data}")
            return None

        k = data[0]
        try:
            return {
                "open_time": int(k[0]),
                "open": float(k[1]),
                "high": float(k[2]),
                "low": float(k[3]),
                "close": float(k[4]),
                "volume": float(k[5]),
                "close_time": int(k[6]),
            }
        except Exception as e:
            FileLogger.error(f"Error parsing kline for {self.symbol}: {e}")
            return None

    # ------------------------------------------------------------
    # Risk action -> execution decision
    # ------------------------------------------------------------
    def _map_risk_action_to_decision(self, risk_action: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not risk_action or not isinstance(risk_action, dict):
            return None

        action = str(risk_action.get("action", "")).upper()
        side = str(risk_action.get("side", "")).upper()
        size = float(risk_action.get("size", 0) or 0)

        if size <= 0:
            return None

        if action not in ["OPEN", "CLOSE", "REDUCE"]:
            return None

        if side == "LONG":
            exec_side = "BUY" if action == "OPEN" else "SELL"
        elif side == "SHORT":
            exec_side = "SELL" if action == "OPEN" else "BUY"
        else:
            return None

        return {"side": exec_side, "type": "MARKET", "size": size}

    # ------------------------------------------------------------
    # Core loop
    # ------------------------------------------------------------
    def _should_process_candle(self, candle: Dict[str, Any]) -> bool:
        close_time = candle.get("close_time")
        if close_time is None:
            return False
        if self.last_kline_close_time_ms is None:
            return True
        return int(close_time) > int(self.last_kline_close_time_ms)

    def run(self) -> None:
        FileLogger.info("LiveLoop started (SAFE MODE ENABLED)")

        while True:
            try:
                candle = self._get_latest_kline()
                if candle and self._should_process_candle(candle):
                    self.last_kline_close_time_ms = candle["close_time"]

                    result = self.engine.on_candle(candle)
                    risk_action = result.get("risk_action") if isinstance(result, dict) else None

                    if not risk_action:
                        continue

                    FileLogger.info("Risk action: " + json.dumps(risk_action))

                    decision = self._map_risk_action_to_decision(risk_action)
                    if not decision:
                        FileLogger.info("Risk action ignored (no executable decision)")
                        continue

                    if not self.allow_live:
                        FileLogger.info("Live trading disabled by config. Execution skipped.")
                        continue

                    if self.dry_run:
                        FileLogger.info("DRY RUN: decision=" + json.dumps(decision))
                        continue

                    if not self.exec_router:
                        FileLogger.error("Execution router not initialized. Skipping execution.")
                        continue

                    exec_result = self.exec_router.route(decision, self.symbol)
                    FileLogger.info("Execution result: " + json.dumps(exec_result))
                    print("Execution result:", exec_result)

            except KeyboardInterrupt:
                FileLogger.info("LiveLoop interrupted by user")
                break
            except Exception as e:
                FileLogger.error(f"LiveLoop error: {e}")
                time.sleep(2)

            time.sleep(1.0)

        FileLogger.info("LiveLoop stopped")


def main() -> None:
    loop = LiveLoop(
        symbol="SOLUSDT",
        interval="1h",
        equity_refresh_seconds=10,
        config_path="config.json",
    )
    loop.run()


if __name__ == "__main__":
    main()
