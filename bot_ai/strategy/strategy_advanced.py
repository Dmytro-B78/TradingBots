# ================================================================
# File: bot_ai/strategy/strategy_advanced.py
# NT-Tech advanced strategy engine (optimized)
# ASCII-only
# ================================================================

from bot_ai.engine.indicators_advanced import IndicatorsAdvanced
from bot_ai.engine.strategy_filters import StrategyFilters
from bot_ai.engine.order_engine import OrderEngine
from bot_ai.engine.file_logger import FileLogger


class StrategyAdvanced:
    """
    NT-Tech optimized advanced strategy engine using:
        - precomputed MA series
        - precomputed RSI / ATR / trend series
        - integrated risk management
        - linear-time processing for millions of candles
    """

    def __init__(self, params, initial_balance, risk_manager):
        self.params = params if isinstance(params, dict) else {}
        try:
            self.initial_balance = float(initial_balance)
        except Exception:
            self.initial_balance = 0.0

        self.risk_manager = risk_manager

        self.engine = OrderEngine(fee_rate=0.001)
        self.engine.set_initial_balance(self.initial_balance)

        self.debug = []

    # ------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------
    def run(self, candles):
        if not isinstance(candles, list) or len(candles) == 0:
            return {
                "initial_balance": self.initial_balance,
                "final_value": self.initial_balance,
                "params": self.params,
                "trades": [],
                "debug": [{"error": "Invalid candle data"}]
            }

        closes = [c["close"] for c in candles]

        # ------------------------------------------------------------
        # Precompute indicators
        # ------------------------------------------------------------
        ma_type = self.params.get("ma_type", "SMA")
        short_p = self.params.get("short_ma", 5)
        long_p = self.params.get("long_ma", 20)

        if ma_type == "EMA":
            short_ma_series = IndicatorsAdvanced.ema_series(closes, short_p)
            long_ma_series = IndicatorsAdvanced.ema_series(closes, long_p)
        elif ma_type == "WMA":
            short_ma_series = IndicatorsAdvanced.wma_series(closes, short_p)
            long_ma_series = IndicatorsAdvanced.wma_series(closes, long_p)
        elif ma_type == "HMA":
            short_ma_series = IndicatorsAdvanced.hma_series(closes, short_p)
            long_ma_series = IndicatorsAdvanced.hma_series(closes, long_p)
        else:
            short_ma_series = IndicatorsAdvanced.sma_series(closes, short_p)
            long_ma_series = IndicatorsAdvanced.sma_series(closes, long_p)

        rsi_period = self.params.get("rsi_period", 14)
        rsi_series = StrategyFilters.rsi_series(closes, rsi_period)

        atr_period = self.params.get("atr_period", 14)
        atr_series = StrategyFilters.atr_series(candles, atr_period)

        trend_period = self.params.get("trend_ma", 20)
        trend_series = StrategyFilters.trend_series(closes, trend_period)

        # ------------------------------------------------------------
        # Main candle loop
        # ------------------------------------------------------------
        for i in range(len(candles)):
            price = closes[i]

            short_ma = short_ma_series[i]
            long_ma = long_ma_series[i]
            rsi_val = rsi_series[i]
            atr_val = atr_series[i]
            slope_val = trend_series[i]

            if short_ma is None or long_ma is None:
                continue
            if rsi_val is None or atr_val is None or slope_val is None:
                continue

            # ------------------------------------------------------------
            # Debug snapshot (reduced)
            # ------------------------------------------------------------
            if i % 1000 == 0:
                self.debug.append({
                    "i": i,
                    "price": price,
                    "short_ma": short_ma,
                    "long_ma": long_ma,
                    "rsi": rsi_val,
                    "atr": atr_val,
                    "trend_slope": slope_val,
                    "position": self.engine.position
                })

            # ------------------------------------------------------------
            # Risk checks
            # ------------------------------------------------------------
            if self.engine.position > 0 and self.engine.entry_price is not None:

                if self.risk_manager.stop_loss_triggered(self.engine.entry_price, price):
                    self.engine.sell(price)
                    FileLogger.info("STOP LOSS at " + str(price))
                    continue

                if self.risk_manager.take_profit_triggered(self.engine.entry_price, price):
                    self.engine.sell(price)
                    FileLogger.info("TAKE PROFIT at " + str(price))
                    continue

                equity = self.engine.equity(price)
                if self.risk_manager.drawdown_triggered(equity):
                    self.engine.sell(price)
                    FileLogger.info("DRAWDOWN EXIT at " + str(price))
                    continue

            # ------------------------------------------------------------
            # Signals
            # ------------------------------------------------------------
            oversold = rsi_val <= self.params.get("rsi_oversold", 30)
            overbought = rsi_val >= self.params.get("rsi_overbought", 70)

            buy_signal = (
                short_ma > long_ma and
                (oversold or rsi_val < 50) and
                self.engine.position == 0
            )

            sell_signal = (
                short_ma < long_ma and
                overbought and
                self.engine.position > 0
            )

            # ------------------------------------------------------------
            # BUY
            # ------------------------------------------------------------
            if buy_signal:
                if self.risk_manager.position_allowed(self.engine.balance, price):
                    trade = self.engine.buy(price)
                    if trade:
                        FileLogger.info("BUY at " + str(price))
                        self.debug.append({"signal": "BUY", "price": price})
                continue

            # ------------------------------------------------------------
            # SELL
            # ------------------------------------------------------------
            if sell_signal:
                trade = self.engine.sell(price)
                if trade:
                    FileLogger.info("SELL at " + str(price))
                    self.debug.append({"signal": "SELL", "price": price})
                continue

        # ------------------------------------------------------------
        # Final equity
        # ------------------------------------------------------------
        final_value = self.engine.equity(closes[-1])

        return {
            "initial_balance": self.initial_balance,
            "final_value": final_value,
            "params": self.params,
            "trades": self.engine.get_trades(),
            "debug": self.debug
        }
