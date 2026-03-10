# ============================================
# File: bot_ai/core/order_manager.py
# Purpose: Basic order manager for strategy integration
# Format: UTF-8 without BOM
# Compatible with RSIReversalStrategy
# ============================================

import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, client=None, test_mode=True):
        self.client = client
        self.test_mode = test_mode
        self.last_order = {}

    def submit_order(self, symbol, side, price, quantity=None):
        logger.info(f"Submitting order | Symbol: {symbol} | Side: {side} | Price: {price:.4f}")

        if self.test_mode or self.client is None:
            logger.info(f"[TEST MODE] Order simulated: {side.upper()} {symbol} @ {price:.4f}")
            self.last_order[symbol] = {"side": side, "price": Decimal(price)}
            return

        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side.upper(),
                type="MARKET",
                quoteOrderQty=round(quantity or 50, 2)  # fallback to 50 USDT if quantity not specified
            )
            logger.info(f"Order executed: {order}")
            self.last_order[symbol] = {"side": side, "price": Decimal(price)}
        except Exception as e:
            logger.error(f"Order failed: {e}")
