# ============================================
# File: bot_ai/db.py
# Purpose: SQLite storage for trades and signals
# Encoding: UTF-8 without BOM
# ============================================

import sqlite3
from datetime import datetime

DB_PATH = "trades.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            action TEXT,
            price REAL,
            time TEXT,
            balance REAL,
            equity REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_trade(trade: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        INSERT INTO trades (symbol, action, price, time, balance, equity)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        trade.get("symbol"),
        trade.get("signal"),
        trade.get("price"),
        trade.get("time").isoformat() if isinstance(trade.get("time"), datetime) else str(trade.get("time")),
        trade.get("balance"),
        trade.get("equity")
    ))
    conn.commit()
    conn.close()

def get_trade_history(symbol=None, limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if symbol:
        c.execute('''
            SELECT * FROM trades WHERE symbol = ? ORDER BY time DESC LIMIT ?
        ''', (symbol, limit))
    else:
        c.execute('''
            SELECT * FROM trades ORDER BY time DESC LIMIT ?
        ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows
