# state_manager.py
# Назначение: Управление текущим балансом и открытыми позициями
# Структура:
# └── bot_ai/core/state_manager.py

_balance = 10000
_positions = []

def get_balance():
    return _balance

def update_balance(amount):
    global _balance
    _balance += amount

def get_positions():
    return _positions

def add_position(position):
    _positions.append(position)

def clear_positions():
    _positions.clear()
