# -*- coding: utf-8 -*-
# === bot_ai/pipeline.py ===
# Основной пайплайн: загрузка данных, генерация сигнала, расчёт позиции,
# контроль времени удержания, логирование

import json
import logging
import os
from datetime import datetime, timedelta

from bot_ai.risk.risk_manager import RiskManager
from bot_ai.strategy.strategy_selector import select_strategy
from bot_ai.utils.data import fetch_ohlcv
from bot_ai.utils.state_manager import load_state, save_state

# === Настройка логирования ===
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/pipeline.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

# === Загрузка конфигурации ===

def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# === Преобразование строки '12h' или '30m' в timedelta ===

def parse_duration(duration_str):
    if duration_str.endswith("h"):
        return timedelta(hours=int(duration_str[:-1]))
    elif duration_str.endswith("m"):
        return timedelta(minutes=int(duration_str[:-1]))
    else:
        return timedelta(0)

# === Основной запуск пайплайна ===

def run_pipeline():
    cfg = load_config()
    strategy_name = cfg.get("strategy", "adaptive")
    pair = cfg.get("symbol", "BTCUSDT")
    timeframe = cfg.get("timeframe", "15m")

    logging.info(
        f"Запуск пайплайна: стратегия={strategy_name}, символ={pair}, таймфрейм={timeframe}")

    # === Загрузка данных ===
    df = fetch_ohlcv(pair, timeframe)
    if df is None or df.empty:
        logging.warning("Нет данных с биржи")
        print("[PIPELINE] ? Нет данных")
        return

    # === Загрузка состояния ===
    state = load_state()
    if "position_opened_at" not in state:
        state["position_opened_at"] = None

    # === Проверка времени удержания позиции ===
    if state["position_opened_at"]:
        max_hold = parse_duration(cfg.get("max_hold", "12h"))
        opened_at = datetime.fromisoformat(state["position_opened_at"])
        now = datetime.utcnow()
        if now - opened_at > max_hold:
            logging.info("Время удержания превышено — закрываем позицию")
            print("[PIPELINE] ? Время удержания превышено — закрываем позицию")
            state["position_opened_at"] = None
            save_state(state)
            return

    # === Выбор стратегии ===
    strategy = select_strategy(strategy_name)
    if strategy is None:
        logging.error(f"Стратегия '{strategy_name}' не найдена")
        print(f"[PIPELINE] ? Стратегия '{strategy_name}' не найдена")
        return

    # === Генерация сигнала ===
    signal = strategy(pair, df, cfg)
    logging.info(f"Сигнал: {signal}")
    print(f"[PIPELINE] ?? Сигнал: {signal}")

    # === Обработка сигнала ===
    if signal and signal[0].get("side") in {"BUY", "SELL"}:
        risk_mgr = RiskManager(cfg)
        position = risk_mgr.execute(signal[0])
        if position:
            logging.info(f"Открытие позиции: {position}")
            print(f"[PIPELINE] ? Позиция: {position}")
            state["position_opened_at"] = signal[0].get(
                "timestamp") or datetime.utcnow().isoformat()
            save_state(state)
        else:
            logging.info("Сделка отклонена RiskManager'ом")
            print("[PIPELINE] ? Сделка отклонена RiskManager'ом")
    else:
        logging.info("Нет сигнала на вход")
        print("[PIPELINE] ? Нет сигнала на вход")

# === Точка входа ===
if __name__ == "__main__":
    run_pipeline()
