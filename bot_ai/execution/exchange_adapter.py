# ================================================================
# File: bot_ai/execution/exchange_adapter.py
# Module: execution.exchange_adapter
# Purpose: NT-Tech Binance Spot exchange adapter
# Responsibilities:
#   - Send real orders to Binance Spot REST API
#   - Query order status
#   - Cancel orders
#   - Normalize responses for execution layer
# Notes:
#   - ASCII-only
#   - Supports mainnet and testnet via environment variable BINANCE_TESTNET
# ================================================================

import os
import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode

from bot_ai.execution.execution_errors import (
    ExecutionError,
    OrderRejectedError
)


class BinanceSpotAdapter:
    """
    NT-Tech Binance Spot adapter.

    Automatically selects:
        - Mainnet: https://api.binance.com
        - Testnet: https://testnet.binance.vision

    Based on environment variable:
        BINANCE_TESTNET=true|false
    """

    MAINNET_URL = "https://api.binance.com"
    TESTNET_URL = "https://testnet.binance.vision"

    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret.encode()

        use_testnet = os.getenv("BINANCE_TESTNET", "true").lower() == "true"
        self.base_url = self.TESTNET_URL if use_testnet else self.MAINNET_URL

    # ------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------
    def _headers(self):
        return {
            "X-MBX-APIKEY": self.api_key
        }

    def _sign(self, params):
        query = urlencode(params)
        signature = hmac.new(
            self.api_secret,
            query.encode(),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def _request(self, method, path, params=None):
        url = self.base_url + path

        if params is None:
            params = {}

        params["timestamp"] = int(time.time() * 1000)
        signed = self._sign(params)

        try:
            if method == "GET":
                r = requests.get(url, params=signed, headers=self._headers(), timeout=10)
            elif method == "POST":
                r = requests.post(url, params=signed, headers=self._headers(), timeout=10)
            elif method == "DELETE":
                r = requests.delete(url, params=signed, headers=self._headers(), timeout=10)
            else:
                raise ExecutionError(f"Unsupported HTTP method: {method}")

            data = r.json()

            if r.status_code != 200:
                msg = data.get("msg", "Unknown error")
                raise ExecutionError(f"Binance error: {msg}")

            return data

        except Exception as e:
            raise ExecutionError(f"HTTP request failed: {str(e)}")

    # ------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------
    def send_order(self, order):
        symbol = order["symbol"]
        side = order["side"]
        size = order["size"]
        order_type = order["type"]

        # MARKET
        if order_type == "MARKET":
            params = {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": size
            }
            data = self._request("POST", "/api/v3/order", params)
            return {
                "order_id": str(data["orderId"]),
                "raw": data
            }

        # LIMIT
        if order_type == "LIMIT":
            params = {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "timeInForce": "GTC",
                "quantity": size,
                "price": order["price"]
            }
            data = self._request("POST", "/api/v3/order", params)
            return {
                "order_id": str(data["orderId"]),
                "raw": data
            }

        # STOP_MARKET
        if order_type == "STOP_MARKET":
            params = {
                "symbol": symbol,
                "side": side,
                "type": "STOP_LOSS",
                "quantity": size,
                "stopPrice": order["stop_price"]
            }
            data = self._request("POST", "/api/v3/order", params)
            return {
                "order_id": str(data["orderId"]),
                "raw": data
            }

        # STOP_LIMIT
        if order_type == "STOP_LIMIT":
            params = {
                "symbol": symbol,
                "side": side,
                "type": "STOP_LOSS_LIMIT",
                "timeInForce": "GTC",
                "quantity": size,
                "price": order["limit_price"],
                "stopPrice": order["stop_price"]
            }
            data = self._request("POST", "/api/v3/order", params)
            return {
                "order_id": str(data["orderId"]),
                "raw": data
            }

        # OCO
        if order_type == "OCO":
            tp = order["take_profit"]
            sl = order["stop_loss"]

            params = {
                "symbol": symbol,
                "side": side,
                "quantity": size,
                "price": tp["price"],
                "stopPrice": sl["stop_price"],
                "stopLimitPrice": sl["limit_price"],
                "stopLimitTimeInForce": "GTC"
            }

            data = self._request("POST", "/api/v3/order/oco", params)
            return {
                "order_id": str(data["orderListId"]),
                "raw": data
            }

        raise ExecutionError(f"Unsupported order type: {order_type}")

    # ------------------------------------------------------------
    # Order status
    # ------------------------------------------------------------
    def get_order_status(self, order_id, symbol=None):
        if symbol is None:
            raise ExecutionError("Symbol required for get_order_status")

        params = {
            "symbol": symbol,
            "orderId": order_id
        }

        data = self._request("GET", "/api/v3/order", params)

        status = data.get("status", "UNKNOWN")
        filled = float(data.get("executedQty", 0.0))
        orig = float(data.get("origQty", 0.0))
        remaining = max(orig - filled, 0.0)

        if status == "REJECTED":
            raise OrderRejectedError(f"Order rejected: {order_id}")

        if status in ("NEW", "PARTIALLY_FILLED", "FILLED"):
            mapped = {
                "NEW": "NEW",
                "PARTIALLY_FILLED": "PARTIAL",
                "FILLED": "FILLED"
            }[status]

            return {
                "status": mapped,
                "filled": filled,
                "remaining": remaining,
                "raw": data
            }

        return {
            "status": "UNKNOWN",
            "filled": filled,
            "remaining": remaining,
            "raw": data
        }

    # ------------------------------------------------------------
    # Cancel order
    # ------------------------------------------------------------
    def cancel_order(self, order_id, symbol):
        params = {
            "symbol": symbol,
            "orderId": order_id
        }

        data = self._request("DELETE", "/api/v3/order", params)

        return {
            "status": "CANCELLED",
            "raw": data
        }
