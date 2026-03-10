# ============================================
# File: bot_ai/strategy/strategy_selector.py
# Purpose: StrategySelector class and default instance
# Format: UTF-8 without BOM
# Compatible with paper_trader and router
# ============================================

from bot_ai.strategy.strategy_loader import load_strategy

class StrategySelector:
    def __init__(self, config):
        self.config = config
        self.strategy_names = config.get("strategies", ["sma"])

    def select(self, context):
        df = context["df"]
        for name in self.strategy_names:
            strategy_class = load_strategy(name)
            instance = strategy_class(self.config)
            signal = instance.generate_signal(df)  # <-- FIXED: only df passed
            if signal:
                return signal
        return None

# === Default selector instance for compatibility ===
strategy_selector = StrategySelector(config={})
# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/strategy/strategy_selector.py
# Purpose: Multi-strategy engine with anti-spam
# Format: UTF-8 without BOM
# Compatible with paper_trader and router
# ============================================

from datetime import datetime

from bot_ai.strategy.strategy_loader import load_strategy

# === Anti-spam memory ===
_last_signal = {
    "side": None,
    "timestamp": None
}

ANTI_SPAM_SECONDS = 300  # 5 minutes


def anti_spam_filter(final_side: str) -> bool:
    """
    Prevent repeated or too frequent signals.
    """
    global _last_signal
    now = datetime.utcnow()

    # First signal ever
    if _last_signal["side"] is None:
        _last_signal["side"] = final_side
        _last_signal["timestamp"] = now
        return True

    # Same signal as before → ignore
    if _last_signal["side"] == final_side:
        return False

    # Too frequent signals
    if _last_signal["timestamp"] and (now - _last_signal["timestamp"]).total_seconds() < ANTI_SPAM_SECONDS:
        return False

    # Update memory
    _last_signal["side"] = final_side
    _last_signal["timestamp"] = now
    return True


class StrategySelector:
    """
    Multi-strategy selector.
    Runs all strategies listed in config["strategies"].
    """

    def __init__(self, config):
        self.config = config
        self.strategy_names = config.get(
            "strategies",
            ["rsi_reversal", "mean_reversion", "breakout"]
        )

    def select(self, context):
        df = context["df"]
        pair = context["pair"]

        results = []

        # Run all strategies
        for name in self.strategy_names:
            strategy_class = load_strategy(name)
            instance = strategy_class(self.config)

            try:
                signal = instance.generate_signal(df)
                side = signal.get("side", "H HOLD") if signal else "HOLD"
            except Exception:
                side = "HOLD"

            results.append({"name": name, "side": side})

        # Count votes
        buy_votes = sum(1 for r in results if r["side"] == "BUY")
        sell_votes = sum(1 for r in results if r["side"] == "SELL")

        if buy_votes >= 2:
            final_side = "BUY"
        elif sell_votes >= 2:
            final_side = "SELL"
        else:
            final_side = "HOLD"

        # Anti-spam
        if not anti_spam_filter(final_side):
            return {"side": "HOLD", "strategies": results}

        # Unified output
        return {
            "side": final_side,
            "timestamp": datetime.utcnow().isoformat(),
            "strategies": results
        }


# === Default selector instance for compatibility ===
strategy_selector = StrategySelector(config={})
# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/strategy/strategy_selector.py
# Purpose: Multi-strategy engine with anti-spam
# Format: UTF-8 without BOM
# Compatible with paper_trader and router
# ============================================

from datetime import datetime

from bot_ai.strategy.strategy_loader import load_strategy

# === Anti-spam memory ===
_last_signal = {
    "side": None,
    "timestamp": None
}

ANTI_SPAM_SECONDS = 300  # 5 minutes


def anti_spam_filter(final_side: str) -> bool:
    """
    Prevent repeated or too frequent signals.
    """
    global _last_signal
    now = datetime.utcnow()

    # First signal ever
    if _last_signal["side"] is None:
        _last_signal["side"] = final_side
        _last_signal["timestamp"] = now
        return True

    # Same signal as before → ignore
    if _last_signal["side"] == final_side:
        return False

    # Too frequent signals
    if _last_signal["timestamp"] and (now - _last_signal["timestamp"]).total_seconds() < ANTI_SPAM_SECONDS:
        return False

    # Update memory
    _last_signal["side"] = final_side
    _last_signal["timestamp"] = now
    return True


class StrategySelector:
    """
    Multi-strategy selector.
    Runs all strategies listed in config["strategies"].
    """

    def __init__(self, config):
        self.config = config
        self.strategy_names = config.get(
            "strategies",
            ["rsi_reversal", "mean_reversion", "breakout"]
        )

    def select(self, context):
        df = context["df"]
        pair = context["pair"]

        results = []

        # Run all strategies
        for name in self.strategy_names:
            strategy_class = load_strategy(name)
            instance = strategy_class(self.config)

            try:
                signal = instance.generate_signal(df)
                side = signal.get("side", "H HOLD") if signal else "HOLD"
            except Exception:
                side = "HOLD"

            results.append({"name": name, "side": side})

        # Count votes
        buy_votes = sum(1 for r in results if r["side"] == "BUY")
        sell_votes = sum(1 for r in results if r["side"] == "SELL")

        if buy_votes >= 2:
            final_side = "BUY"
        elif sell_votes >= 2:
            final_side = "SELL"
        else:
            final_side = "HOLD"

        # Anti-spam
        if not anti_spam_filter(final_side):
            return {"side": "HOLD", "strategies": results}

        # Unified output
        return {
            "side": final_side,
            "timestamp": datetime.utcnow().isoformat(),
            "strategies": results
        }


# === Default selector instance for compatibility ===
strategy_selector = StrategySelector(config={})
