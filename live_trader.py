# -*- coding: utf-8 -*-
# ============================================
# File: live_trader.py
# Назначение: CLI-интерфейс для запуска paper/live-трейдинга
# Поддержка: --config, --mode, --strategy, --adaptive, --symbol, --balance
# Использует: paper_trader, live_trader_engine, strategy_router
# ============================================

import argparse
import json
import logging
import os

# === Настройка логирования ===
def setup_logging():
    os.makedirs("logs", exist_ok=True)
    logging.basicConfig(
        filename="logs/live_trader.log",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

# === Загрузка конфигурации ===
def load_config(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Точка входа ===
def main():
    parser = argparse.ArgumentParser(description="🚀 Live/Paper трейдинг")
    parser.add_argument("--config", type=str, default="config.json", help="Путь к конфигурационному файлу")
    parser.add_argument("--mode", type=str, choices=["paper", "live"], default="paper", help="Режим работы")
    parser.add_argument("--symbol", type=str, help="Торгуемая пара")
    parser.add_argument("--strategy", type=str, help="Имя стратегии")
    parser.add_argument("--adaptive", action="store_true", help="Автоматический выбор стратегии")
    parser.add_argument("--balance", type=float, help="Начальный баланс")
    args = parser.parse_args()

    setup_logging()
    config = load_config(args.config)

    # Переопределение параметров из CLI
    symbol = args.symbol or config.get("symbol") or config.get("symbols", [{}])[0].get("pair")
    strategy = "adaptive" if args.adaptive else (args.strategy or config.get("strategy"))
    balance = args.balance or config.get("capital", 1000)

    cfg = {
        **config,
        "symbol": symbol,
        "strategy": strategy,
        "initial_balance": balance
    }

    print(f"🚀 Запуск {args.mode}-трейдинга | {symbol} | Стратегия: {strategy}")

    if args.mode == "paper":
        from bot_ai.paper_trader import run_trading_loop
    elif args.mode == "live":
        from bot_ai.live_trader_engine import run_trading_loop
    else:
        raise ValueError("Неверный режим. Используй --mode paper или --mode live")

    run_trading_loop(cfg)

if __name__ == "__main__":
    main()
