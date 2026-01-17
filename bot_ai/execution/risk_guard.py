# risk_guard.py
# Назначение: Проверка условий риска перед входом в сделку
# Структура:
# └── bot_ai/exec/risk_guard.py

def is_trade_allowed(trade, config):
    rr = abs(trade["target"] - trade["entry"]) / abs(trade["entry"] - trade["stop"] + 1e-9)
    if rr < config["min_risk_reward_ratio"]:
        print(f"[FILTER:riskguard] ❌ RR={rr:.2f} < min {config['min_risk_reward_ratio']}")
        return False
    return True
