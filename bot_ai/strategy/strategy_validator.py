# strategy_validator.py
# Назначение: Проверка структуры и типов параметров в config.json
# Структура:
# └── bot_ai/strategy/strategy_validator.py

def validate_config(config):
    required_fields = {
        "exchange": str,
        "mode": str,
        "capital": (int, float),
        "risk_per_trade": float,
        "min_risk_reward_ratio": float,
        "stop_loss_pct": float,
        "trailing_stop_pct": float,
        "atr_threshold": float,
        "atr_period": int,
        "adx_threshold": float,
        "adx_period": int,
        "max_holding_period": int
    }

    for key, expected_type in required_fields.items():
        if key not in config:
            raise ValueError(f"❌ Отсутствует параметр: {key}")
        if not isinstance(config[key], expected_type):
            raise ValueError(f"❌ Неверный тип для {key}: ожидался {expected_type}, получен {type(config[key])}")

    if config["mode"] not in ["backtest", "paper", "live"]:
        raise ValueError(f"❌ Недопустимый режим: {config['mode']}")

    return True
