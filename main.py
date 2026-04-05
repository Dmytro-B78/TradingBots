# ================================================================
# File: main.py
# NT-Tech main entry point for backtesting
# ASCII-only
# ================================================================

import sys
import json
import os

from bot_ai.engine.data_loader import DataLoader
from bot_ai.engine.config_loader import ConfigLoader
from bot_ai.engine.strategy_router import StrategyRouter
from bot_ai.engine.trade_analyzer import TradeAnalyzer
from bot_ai.engine.file_logger import FileLogger


def main():

    # ------------------------------------------------------------
    # Load config
    # ------------------------------------------------------------
    try:
        config = ConfigLoader.load_from_json("config.json")
        FileLogger.info("Config loaded successfully")
    except Exception as e:
        print("Config load error: " + str(e))
        FileLogger.error("Config load error: " + str(e))
        return

    # ------------------------------------------------------------
    # Validate strategy section
    # ------------------------------------------------------------
    if "meta_strategy" not in config:
        msg = "Missing required config section: meta_strategy"
        print(msg)
        FileLogger.error(msg)
        return

    # ------------------------------------------------------------
    # Load candles.json which contains directory path
    # ------------------------------------------------------------
    try:
        with open("candles.json", "r", encoding="utf-8") as f:
            c = json.load(f)

        if "source" not in c:
            raise Exception("candles.json must contain 'source' field")

        source_path = c["source"]

        if not os.path.exists(source_path):
            raise Exception("Source path does not exist: " + str(source_path))

        candles = DataLoader.load(source_path)

        if not candles:
            raise Exception("No candles loaded")

        FileLogger.info("Candles loaded: " + str(len(candles)))
        print("Total candles:", len(candles))

    except Exception as e:
        print("Candle load error: " + str(e))
        FileLogger.error("Candle load error: " + str(e))
        return

    # ------------------------------------------------------------
    # Run strategy
    # ------------------------------------------------------------
    try:
        router = StrategyRouter(config)
        result = router.run(candles)

        if not isinstance(result, dict):
            raise Exception("Strategy returned invalid result")

        if "trades" not in result:
            raise Exception("Strategy result missing 'trades' field")

        FileLogger.info("Strategy executed successfully")

    except Exception as e:
        print("Strategy error: " + str(e))
        FileLogger.error("Strategy error: " + str(e))
        return

    # ------------------------------------------------------------
    # Analyze trades
    # ------------------------------------------------------------
    try:
        trades = result.get("trades", [])

        analyzer = TradeAnalyzer(
            trades,
            result.get("initial_balance", 0),
            result.get("final_value", 0)
        )
        stats = analyzer.summary()

        FileLogger.info("Trade analysis completed")

    except Exception as e:
        print("Trade analysis error: " + str(e))
        FileLogger.error("Trade analysis error: " + str(e))
        return

    # ------------------------------------------------------------
    # Output
    # ------------------------------------------------------------
    print("================================================")
    print(" NT-Tech Strategy Report")
    print("================================================")
    print("Initial balance:", result.get("initial_balance", 0))
    print("Final value:    ", result.get("final_value", 0))
    print("------------------------------------------------")
    print("Trades:")
    for t in trades:
        print(t)
    print("------------------------------------------------")
    print("Statistics:")
    for k, v in stats.items():
        print(k + ":", v)

    FileLogger.info("NT-Tech run completed")


if __name__ == "__main__":
    main()
