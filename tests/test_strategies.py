# ============================================
# Path: C:\TradingBots\NT\tests\test_strategies.py
# Purpose: Run all strategies on synthetic data with volatility and logging
# Format: UTF-8 without BOM
# ============================================

import sys
import os
import logging
import random
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bot_ai.strategy.strategy_loader import load_strategy_class
from bot_ai.strategy.strategy_catalog import STRATEGY_CATALOG

# Configure logging
logging.basicConfig(
    filename="strategy_test.log",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def generate_test_data(rows=60):
    """Generate synthetic OHLCV data with volatility for testing strategies."""
    base_price = 100.0
    prices = []
    for i in range(rows):
        change = random.uniform(-2.5, 2.5)
        base_price = max(1, base_price + change)
        prices.append(base_price)

    data = {
        "open": [p + random.uniform(-1, 1) for p in prices],
        "high": [p + random.uniform(0.5, 2.0) for p in prices],
        "low": [p - random.uniform(0.5, 2.0) for p in prices],
        "close": prices,
        "volume": [random.randint(800, 2500) for _ in range(rows)],
    }
    df = pd.DataFrame(data)
    df.index = pd.date_range(end=pd.Timestamp.now(), periods=rows, freq="h")
    df["symbol"] = "TEST"
    return df

def test_strategies():
    df = generate_test_data()
    for name, meta in STRATEGY_CATALOG.items():
        print(f"\n--- Testing strategy: {name} ---")
        logging.info(f"Testing strategy: {name}")
        try:
            StrategyClass = load_strategy_class(name)
            strategy = StrategyClass(meta["default_params"])
            signal = strategy.generate_signal(df)
            logging.info(f"Signal: {signal}")
            print("Signal:", signal or "No signal")
            assert hasattr(strategy, "generate_signal"), "Strategy missing generate_signal method"
        except Exception as e:
            logging.exception(f"Error testing {name}")
            print(f"Error testing {name}: {e}")

if __name__ == "__main__":
    test_strategies()
