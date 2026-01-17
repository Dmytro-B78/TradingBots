# position_tracker.py
# Назначение: Управление активными позициями (в live-режиме)
# Структура:
# └── bot_ai/exec/position_tracker.py

positions = []

def add_position(pos):
    positions.append(pos)

def get_open_positions():
    return positions

def close_position(symbol):
    global positions
    positions = [p for p in positions if p["symbol"] != symbol]
