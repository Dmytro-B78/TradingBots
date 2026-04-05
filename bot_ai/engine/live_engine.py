# ================================================================
# File: bot_ai/engine/live_engine.py
# NT-Tech Live Engine 3.0 (Strict Mode C, ASCII-only)
# ================================================================

import os
import time
import math
import traceback
from dotenv import load_dotenv
from binance.spot import Spot

from bot_ai.engine.file_logger import FileLogger
from bot_ai.strategy.meta_strategy import MetaStrategy


class LiveEngine:
    """
    NT-Tech Live Engine 3.0
    Strict Mode C:
        - allow_live_trading is loaded ONLY from config.json
        - dry_run can be overridden from scripts
        - real trading requires BOTH:
            allow_live_trading = True
            dry_run = False
    """

    def __init__(
        self,
        config,
        position_pct=1.0,
        min_volume=50000000,
        dry_run=True
    ):
        load_dotenv("C:\\TradingBots\\NT\\.env")

        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")

        self.client = Spot(key=api_key, secret=api_secret)

        # MetaStrategy receives full config
        self.meta = MetaStrategy(config)

        # Strict Mode C
        self.allow_live_trading = bool(config.get("allow_live_trading", False))
        self.dry_run = bool(dry_run)

        self.position_pct = float(position_pct)
        self.min_volume = float(min_volume)

        self.symbol = None
        self.position = "FLAT"
        self.entry_price = None
        self.amount = 0.0
        self.sl = None
        self.tp = None

        FileLogger.info("LiveEngine initialized")
        FileLogger.info("allow_live_trading=" + str(self.allow_live_trading))
        FileLogger.info("dry_run=" + str(self.dry_run))

    # ------------------------------------------------------------
    # Fail-safe order wrapper
    # ------------------------------------------------------------
    def safe_order(self, side, amount):
        """
        Real orders allowed ONLY if:
            allow_live_trading == True
            dry_run == False
        """

        if self.dry_run:
            FileLogger.info("DRY-RUN ORDER: " + side + " amount=" + str(amount))
            return {"dry_run": True, "side": side, "amount": amount}

        if not self.allow_live_trading:
            FileLogger.warn("FAIL-SAFE BLOCK: Real trading disabled by config.json")
            return {"blocked": True, "side": side, "amount": amount}

        return self.client.new_order(
            symbol=self.symbol,
            side=side,
            type="MARKET",
            quantity=amount
        )

    # ------------------------------------------------------------
    # Market Scanner
    # ------------------------------------------------------------
    def scan_markets(self):
        tickers = self.client.ticker_24hr()

        usdt_pairs = []
        for t in tickers:
            symbol = t.get("symbol", "")
            if symbol.endswith("USDT"):
                try:
                    vol = float(t.get("quoteVolume", 0))
                    if vol >= self.min_volume:
                        usdt_pairs.append((symbol, vol))
                except Exception:
                    continue

        usdt_pairs.sort(key=lambda x: x[1], reverse=True)

        if not usdt_pairs:
            raise Exception("No USDT pairs found above volume threshold")

        self.symbol = usdt_pairs[0][0]
        FileLogger.info("Selected symbol: " + self.symbol)
        return self.symbol

    # ------------------------------------------------------------
    # Price Feed
    # ------------------------------------------------------------
    def get_price(self):
        data = self.client.ticker_price(self.symbol)
        return float(data["price"])

    # ------------------------------------------------------------
    # Position Sizing
    # ------------------------------------------------------------
    def compute_amount(self, price):
        acc = self.client.account()
        balances = acc.get("balances", [])

        usdt = 0.0
        for b in balances:
            if b["asset"] == "USDT":
                usdt = float(b["free"])
                break

        trade_usdt = usdt * self.position_pct
        if trade_usdt <= 0:
            return 0.0

        amount = trade_usdt / price
        amount = math.floor(amount * 10000) / 10000
        return amount

    # ------------------------------------------------------------
    # Trade Execution
    # ------------------------------------------------------------
    def open_long(self, price):
        amount = self.compute_amount(price)
        if amount <= 0:
            return None

        order = self.safe_order("BUY", amount)

        self.position = "LONG"
        self.entry_price = price
        self.amount = amount

        self.sl = self.meta.sl
        self.tp = self.meta.tp

        FileLogger.info(
            f"OPEN_LONG {self.symbol} price={price} amount={amount} sl={self.sl} tp={self.tp}"
        )

        return order

    def close_long(self, price, reason):
        if self.position != "LONG":
            return None

        order = self.safe_order("SELL", self.amount)

        pnl = (price - self.entry_price) * self.amount

        FileLogger.info(
            f"CLOSE_LONG {self.symbol} price={price} amount={self.amount} pnl={pnl} reason={reason}"
        )

        self.position = "FLAT"
        self.entry_price = None
        self.amount = 0.0
        self.sl = None
        self.tp = None

        return order

    # ------------------------------------------------------------
    # Main Loop
    # ------------------------------------------------------------
    def run(self, interval=2):
        if not self.symbol:
            self.scan_markets()

        while True:
            try:
                price = self.get_price()
                candle = {"close": price}

                signal = self.meta.on_candle(candle)

                if signal:
                    sig = signal.get("signal")

                    if sig == "OPEN_LONG" and self.position == "FLAT":
                        self.open_long(price)

                    elif sig == "CLOSE_LONG" and self.position == "LONG":
                        self.close_long(price, signal.get("reason"))

                if self.position == "LONG":
                    if price <= self.sl:
                        self.close_long(price, "SL")
                    elif price >= self.tp:
                        self.close_long(price, "TP")

            except Exception as e:
                FileLogger.error("ERROR: " + str(e))
                FileLogger.error(traceback.format_exc())
                time.sleep(5)

            time.sleep(interval)
