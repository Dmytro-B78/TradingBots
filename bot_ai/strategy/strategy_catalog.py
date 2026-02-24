# ============================================
# File: bot_ai/strategy/strategy_catalog.py
# Purpose: Central registry of available strategies and their default parameters
# Format: UTF-8 without BOM
# Compatible with: strategy loader, adaptive engine
# ============================================

STRATEGY_CATALOG = {
    "breakout": {
        "class": "BreakoutStrategy",
        "module": "bot_ai.strategy.breakout",
        "default_params": {
            "window": 20,
            "buffer_pct": 0.001,
            "min_volume": 0
        }
    },
    "mean_reversion": {
        "class": "MeanReversionStrategy",
        "module": "bot_ai.strategy.mean_reversion",
        "default_params": {
            "window": 20,
            "std_dev": 2.0
        }
    },
    "rsi_macd": {
        "class": "RSIMACDStrategy",
        "module": "bot_ai.strategy.rsi_macd",
        "default_params": {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70,
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9
        }
    },
    "ma_crossover": {
        "class": "MACrossoverStrategy",
        "module": "bot_ai.strategy.ma_crossover_strategy",
        "default_params": {
            "fast_period": 9,
            "slow_period": 21
        }
    },
    "range": {
        "class": "RangeStrategy",
        "module": "bot_ai.strategy.range",
        "default_params": {
            "window": 20,
            "buffer_pct": 0.001,
            "min_volume": 0
        }
    },
    "rsi_reversal": {
        "class": "RSIReversalStrategy",
        "module": "bot_ai.strategy.rsi_reversal_strategy",
        "default_params": {
            "rsi_period": 14,
            "rsi_oversold": 30,
            "rsi_overbought": 70
        }
    },
    "sma_reversal": {
        "class": "SMAReversalStrategy",
        "module": "bot_ai.strategy.sma_reversal_strategy",
        "default_params": {
            "sma_period": 20
        }
    },
    "volume_spike": {
        "class": "VolumeSpikeStrategy",
        "module": "bot_ai.strategy.volume_spike_strategy",
        "default_params": {
            "volume_window": 20,
            "volume_multiplier": 2.0
        }
    },
    "volatility_breakout": {
        "class": "VolatilityBreakoutStrategy",
        "module": "bot_ai.strategy.volatility_breakout_strategy",
        "default_params": {
            "atr_period": 14,
            "atr_multiplier": 1.5
        }
    },
    "zero_cross": {
        "class": "ZeroCrossStrategy",
        "module": "bot_ai.strategy.zero_cross_strategy",
        "default_params": {
            "macd_fast": 12,
            "macd_slow": 26,
            "macd_signal": 9
        }
    }
}
