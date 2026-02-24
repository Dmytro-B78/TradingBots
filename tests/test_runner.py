# ============================================
# File: C:\TradingBots\NT\tests\test_runner.py
# Purpose: Sanity check for core modules and strategy imports
# Format: UTF-8 without BOM
# ============================================

import os
import sys

try:
    from bot_ai.strategy.rsi_reversal_strategy import RSIReversalStrategy
    from bot_ai.core.order_manager import OrderManager
    from bot_ai.core.signal import Signal
    from bot_ai.indicators import calculate_rsi
    from bot_ai.metrics import calculate_metrics
    from dotenv import load_dotenv
    import pandas as pd
    import json
    import time
    import argparse
    print("✅ All core modules imported successfully.")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Check config file
config_path = "config.json"
if not os.path.exists(config_path):
    print(f"❌ Missing config file: {config_path}")
    sys.exit(1)
else:
    print(f"✅ Config file found: {config_path}")

# Check data folder
data_dir = "data"
if not os.path.exists(data_dir):
    print(f"❌ Missing data folder: {data_dir}")
    sys.exit(1)
else:
    print(f"✅ Data folder found: {data_dir}")

# Check logs folder
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)
    print(f"📁 Created logs folder: {logs_dir}")
else:
    print(f"✅ Logs folder exists: {logs_dir}")

print("🧪 Basic environment check complete.")
