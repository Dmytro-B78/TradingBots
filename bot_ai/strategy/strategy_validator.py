# ============================================
# bot_ai/strategy/strategy_validator.py
# Проверка конфигурации стратегии: обязательные поля, типы, допустимые значения
# Используется для валидации config.json перед запуском
# ============================================

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
            raise ValueError(f"Отсутствует обязательный параметр конфигурации: {key}")
        if not isinstance(config[key], expected_type):
            raise ValueError(f"Неверный тип параметра '{key}': ожидался {expected_type}, получен {type(config[key])}")

    if config["mode"] not in ["backtest", "paper", "live"]:
        raise ValueError(f"Недопустимое значение 'mode': {config['mode']}")

    return True

