# risk_manager.py
# Назначение: Расчёт объёма позиции на основе риска и стопа
# Структура:
# └── bot_ai/strategy/risk_manager.py

def calculate_position(entry_price, stop_price, capital, risk_per_trade):
    risk_amount = capital * risk_per_trade
    risk_per_unit = abs(entry_price - stop_price)
    if risk_per_unit == 0:
        return 0
    position_size = risk_amount / risk_per_unit
    return round(position_size, 4)
