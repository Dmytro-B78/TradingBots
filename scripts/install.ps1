# ================================================================
# NT-Tech Project Skeleton Installer
# File: C:\TradingBots\NT\scripts\install.ps1
#
# Purpose:
#   Creates the full NT-Tech 2026 project folder structure and
#   generates required base files (config, __init__.py, placeholders).
#
# How to run:
#   cd C:\TradingBots\NT\scripts
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#
# Notes:
#   - Existing files will be overwritten
#   - Missing directories will be created automatically
#   - ASCII-only, no Cyrillic
# ================================================================

Write-Host "NT-Tech Installer Started..."

$base = "C:\TradingBots\NT"

# ------------------------------------------------------------
# Create directory structure (NT-Tech 2026)
# ------------------------------------------------------------
New-Item -ItemType Directory -Force -Path "$base" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\backtest" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\selector" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\risk" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\strategy" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\bot_ai\utils" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\logs" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\data" | Out-Null
New-Item -ItemType Directory -Force -Path "$base\scripts" | Out-Null

# ------------------------------------------------------------
# Create config.json (NT-Tech 2026 full config)
# ------------------------------------------------------------
@'
{
    "selector": {
        "all_pairs": ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT"],
        "top_n": 3,
        "min_volume": 50000000,
        "reload_sec": 60
    },

    "backtest": {
        "candles_path": "C:/TradingBots/candles/compiled",
        "lookback_candles": 5000,
        "initial_balance": 10000,
        "timeframe": "1h"
    },

    "live": {
        "dry_run": true,
        "api_enabled": false,
        "allow_live_trading": false,
        "require_manual_confirm": true,
        "cooldown_sec": 5,
        "max_slippage_pct": 0.2,
        "max_position_size_usdt": 500
    },

    "risk": {
        "daily_loss_limit": 0.03,
        "weekly_loss_limit": 0.07,
        "kill_switch": true,

        "risk_engine": {
            "initial_equity": 10000.0,
            "base_risk_pct": 0.0075,
            "max_risk_pct": 0.015,
            "min_risk_pct": 0.0025,
            "stop_mult_base": 1.8,
            "stop_mult_low_vol": 1.4,
            "stop_mult_high_vol": 2.2,
            "stop_mult_extreme_vol": 2.8,
            "atr_ratio_shock": 2.5,
            "shock_risk_scale": 0.5,
            "trend_risk_boost": 1.1,
            "range_risk_scale": 0.8,
            "compression_risk_scale": 0.6,
            "expansion_risk_scale": 1.0,
            "max_exposure_pct": 0.30
        }
    },

    "strategy": {
        "name": "meta_strategy",
        "params": {
            "use_mtf": true,
            "use_atr": true
        }
    },

    "optimizer": {
        "enabled": false,
        "output_dir": "logs/optimizer",

        "sweep": {
            "ema_fast": [5, 8, 10, 12, 14],
            "ema_slow": [20, 30, 40, 50, 60],
            "atr_period": [7, 10, 14, 21],
            "atr_mult": [1.5, 2.0, 2.5, 3.0],
            "breakout_k": [1.5, 2.0, 2.5, 3.0],
            "impulse_thr": [0.5, 1.0, 1.5, 2.0],
            "stop_loss_pct": [0.5, 1.0, 1.5, 2.0],
            "take_profit_pct": [1.0, 2.0, 3.0, 4.0],
            "trailing_mult": [1.0, 1.2, 1.4, 1.6]
        },

        "constraints": {
            "max_combinations": 500,
            "min_trades": 20,
            "max_drawdown_pct": 25
        }
    }
}
'@ | Set-Content "$base\config.json"

# ------------------------------------------------------------
# __init__.py files
# ------------------------------------------------------------
@'
# NT-Tech root package
'@ | Set-Content "$base\bot_ai\__init__.py"

@'
# NT-Tech backtest package
'@ | Set-Content "$base\bot_ai\backtest\__init__.py"

@'
# NT-Tech selector package
'@ | Set-Content "$base\bot_ai\selector\__init__.py"

@'
# NT-Tech risk package
'@ | Set-Content "$base\bot_ai\risk\__init__.py"

@'
# NT-Tech strategy package
'@ | Set-Content "$base\bot_ai\strategy\__init__.py"

@'
# NT-Tech utils package
'@ | Set-Content "$base\bot_ai\utils\__init__.py"

# ------------------------------------------------------------
# Placeholder modules (minimal, safe)
# ------------------------------------------------------------
@'
class RiskGuard:
    def __init__(self):
        pass
'@ | Set-Content "$base\bot_ai\risk\risk_guard.py"

@'
class Strategy:
    def __init__(self):
        pass
'@ | Set-Content "$base\bot_ai\strategy\strategy.py"

@'
def safe_float(v):
    try:
        return float(v)
    except:
        return 0.0
'@ | Set-Content "$base\bot_ai\utils\safe.py"

# ------------------------------------------------------------
# Create empty log file
# ------------------------------------------------------------
"" | Set-Content "$base\logs\night_backtest.log"

Write-Host "NT-Tech Installer Completed."
