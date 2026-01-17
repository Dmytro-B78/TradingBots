# metrics_calculator.py
# Назначение: Расчёт метрик по результатам сделок
# Структура:
# └── bot_ai/analytics/metrics_calculator.py

def calculate_metrics(trades, capital):
    balance = capital
    equity_curve = []

    for trade in trades:
        risk = trade["entry"] - trade["stop"]
        reward = trade["target"] - trade["entry"]
        rr_ratio = reward / risk if risk > 0 else 0

        if rr_ratio >= 1.5:
            balance += reward
        else:
            balance -= risk

        equity_curve.append(round(balance, 2))

    return {
        "total_trades": len(trades),
        "final_balance": round(balance, 2),
        "equity_curve": equity_curve
    }
