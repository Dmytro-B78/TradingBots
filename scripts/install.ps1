# ================================================================
# NT-Tech Project Skeleton Installer
# File: C:\TradingBots\NT\scripts\install.ps1
#
# Purpose:
#   Creates the full NT-Tech project folder structure and generates
#   all required Python files (config, engine modules, main entry).
#
# How to run:
#   1. Open PowerShell as Administrator
#   2. Run:
#        cd C:\TradingBots\NT\scripts
#        powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Notes:
#   - Existing files will be overwritten
#   - Missing directories will be created automatically
# ================================================================

Write-Host "NT-Tech Installer Started..."

$base = "C:\TradingBots\NT"

New-Item -ItemType Directory -Force -Path "$base" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\config" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\engine" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\data" | Out-Null

# ---------------- root __init__.py ----------------
@"
# NT-Tech root package
"@ | Set-Content "$base\bot_ai\__init__.py"

# ---------------- config __init__.py ----------------
@"
from .config import Config
"@ | Set-Content "$base\bot_ai\config\__init__.py"

# ---------------- config.py ----------------
@"
import os

class Config:
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    BACKTEST_DATA_DIR = os.path.join(ROOT_DIR, "data")

    BACKTEST_DEFAULT_SYMBOL = "BTCUSDT"
    BACKTEST_DEFAULT_INTERVAL = "1h"

    INITIAL_BALANCE = 10000.0

    DEFAULT_STRATEGY = "ma_crossover"
    DEFAULT_PARAMS = {
        "short_period": 10,
        "long_period": 30
    }
"@ | Set-Content "$base\bot_ai\config\config.py"

# ---------------- engine __init__.py ----------------
@"
from .data_loader import DataLoader
from .strategy_engine import StrategyEngine
from .order_engine import OrderEngine
from .risk_manager import RiskManager
from .indicators import Indicators
from .logger import Logger
from .live_engine import LiveEngine
from .utils import Utils
"@ | Set-Content "$base\bot_ai\engine\__init__.py"

# ---------------- data_loader.py ----------------
@"
import csv

class DataLoader:
    @staticmethod
    def from_csv(path):
        candles = []
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            required = ["timestamp","open","high","low","close","volume"]
            for r in required:
                if r not in reader.fieldnames:
                    raise ValueError(f"Missing required column: {r}")
            for row in reader:
                candles.append({
                    "timestamp": int(row["timestamp"]),
                    "open": float(row["open"]),
                    "high": float(row["high"]),
                    "low": float(row["low"]),
                    "close": float(row["close"]),
                    "volume": float(row["volume"])
                })
        return candles
"@ | Set-Content "$base\bot_ai\engine\data_loader.py"

# ---------------- indicators.py ----------------
@"
class Indicators:
    @staticmethod
    def sma(values, period):
        if len(values) < period:
            return None
        return sum(values[-period:]) / period

    @staticmethod
    def ema(values, period):
        if len(values) < period:
            return None
        k = 2 / (period + 1)
        ema_val = sum(values[:period]) / period
        for v in values[period:]:
            ema_val = v * k + ema_val * (1 - k)
        return ema_val
"@ | Set-Content "$base\bot_ai\engine\indicators.py"

# ---------------- order_engine.py ----------------
@"
class OrderEngine:
    def __init__(self, fee_rate=0.001):
        self.fee_rate = fee_rate

    def buy(self, balance, price):
        if balance <= 0 or price <= 0:
            return balance, 0.0, None, 0.0
        fee = balance * self.fee_rate
        amount = (balance - fee) / price
        return 0.0, amount, price, fee

    def sell(self, position, price):
        if position <= 0 or price <= 0:
            return 0.0, 0.0, 0.0
        proceeds = position * price
        fee = proceeds * self.fee_rate
        net = proceeds - fee
        return net, 0.0, fee
"@ | Set-Content "$base\bot_ai\engine\order_engine.py"

# ---------------- risk_manager.py ----------------
@"
class RiskManager:
    def __init__(self, max_position_ratio=1.0):
        self.max_position_ratio = max_position_ratio

    def can_enter(self, position):
        return position == 0.0

    def can_exit(self, position):
        return position > 0.0

    def validate_buy(self, balance, price):
        if balance <= 0 or price <= 0:
            return False
        return True

    def validate_sell(self, position, price):
        if position <= 0 or price <= 0:
            return False
        return True
"@ | Set-Content "$base\bot_ai\engine\risk_manager.py"

# ---------------- logger.py ----------------
@"
import datetime

class Logger:
    @staticmethod
    def _ts():
        return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def info(msg):
        print(f"[INFO] {Logger._ts()} | {msg}")

    @staticmethod
    def warn(msg):
        print(f"[WARN] {Logger._ts()} | {msg}")

    @staticmethod
    def error(msg):
        print(f"[ERROR] {Logger._ts()} | {msg}")
"@ | Set-Content "$base\bot_ai\engine\logger.py"

# ---------------- utils.py ----------------
@"
class Utils:
    @staticmethod
    def safe_float(v):
        try:
            return float(v)
        except:
            return 0.0

    @staticmethod
    def safe_int(v):
        try:
            return int(v)
        except:
            return 0

    @staticmethod
    def fmt(v, digits=6):
        try:
            return round(float(v), digits)
        except:
            return v
"@ | Set-Content "$base\bot_ai\engine\utils.py"

# ---------------- live_engine.py ----------------
@"
class LiveEngine:
    def __init__(self):
        self.last_price = None

    def update_price(self, price):
        if price is None or price <= 0:
            return
        self.last_price = price

    def get_price(self):
        return self.last_price
"@ | Set-Content "$base\bot_ai\engine\live_engine.py"

# ---------------- strategy_engine.py ----------------
@"
class StrategyEngine:
    def __init__(self, strategy_name, params, initial_balance):
        self.strategy_name = strategy_name
        self.params = params
        self.initial_balance = float(initial_balance)
        self.balance = float(initial_balance)
        self.position = 0.0
        self.entry_price = None
        self.fee_rate = 0.001
        self.trades = []

    def run_backtest(self, candles):
        if self.strategy_name == "ma_crossover":
            return self._run_ma_crossover(candles)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy_name}")

    def _run_ma_crossover(self, candles):
        short_p = self.params["short_period"]
        long_p = self.params["long_period"]
        closes = [c["close"] for c in candles]

        for i in range(len(candles)):
            if i < long_p:
                continue

            short_ma = sum(closes[i - short_p:i]) / short_p
            long_ma = sum(closes[i - long_p:i]) / long_p
            price = closes[i]

            if short_ma > long_ma and self.position == 0:
                self._buy(price)
            elif short_ma < long_ma and self.position > 0:
                self._sell(price)

        final_value = self._equity(closes[-1])

        return {
            "initial_balance": self.initial_balance,
            "final_value": final_value,
            "strategy": self.strategy_name,
            "params": self.params,
            "trades": self.trades
        }

    def _buy(self, price):
        if self.balance <= 0:
            return
        fee = self.balance * self.fee_rate
        amount = (self.balance - fee) / price
        self.position = amount
        self.entry_price = price
        self.balance = 0.0
        self.trades.append({
            "type": "BUY",
            "price": price,
            "amount": amount,
            "fee": fee
        })

    def _sell(self, price):
        if self.position <= 0:
            return
        proceeds = self.position * price
        fee = proceeds * self.fee_rate
        net = proceeds - fee
        self.balance = net
        self.position = 0.0
        self.trades.append({
            "type": "SELL",
            "price": price,
            "amount": self.position,
            "fee": fee
        })
        self.entry_price = None

    def _equity(self, last_price):
        if self.position > 0:
            return self.balance + self.position * last_price
        return self.balance
"@ | Set-Content "$base\bot_ai\engine\strategy_engine.py"

# ---------------- main.py ----------------
@"
import os
from bot_ai.config.config import Config
from bot_ai.engine.data_loader import DataLoader
from bot_ai.engine.strategy_engine import StrategyEngine

def build_csv_path():
    symbol = Config.BACKTEST_DEFAULT_SYMBOL
    interval = Config.BACKTEST_DEFAULT_INTERVAL
    directory = Config.BACKTEST_DATA_DIR
    filename = f"{symbol}-{interval}.csv"
    return os.path.join(directory, filename)

def main():
    csv_path = build_csv_path()
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Candle file not found: {csv_path}")

    candles = DataLoader.from_csv(csv_path)
    engine = StrategyEngine(
        strategy_name=Config.DEFAULT_STRATEGY,
        params=Config.DEFAULT_PARAMS,
        initial_balance=Config.INITIAL_BALANCE
    )
    result = engine.run_backtest(candles)

    print("================================================")
    print("NT-Tech Backtest Result")
    print("================================================")
    print(result)

if __name__ == "__main__":
    main()
"@ | Set-Content "$base\main.py"

Write-Host "NT-Tech Installer Completed."
