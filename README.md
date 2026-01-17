# 🤖 TradingBots

AI‑адаптивный торговый бот с прозрачной архитектурой, строгим контролем рисков и системой уведомлений.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Tests](https://img.shields.io/badge/tests-100%25-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 🚀 Возможности

- 📊 Автоматический отбор торговых пар (D1 + LTF)
- 🎯 Динамические SL/TP с учётом волатильности
- 🛡 RiskGuard: дневные лимиты, kill-switch, cooldown
- 📬 Централизованная система уведомлений (Telegram)
- 🧠 Модульная архитектура стратегий
- 🧪 Поддержка режимов: backtest, paper, live
- 📈 Walk-Forward анализ и логирование сделок
- 🧾 Конфигурация через `config.json`

---

## 📈 Поддерживаемые стратегии

| Название        | Файл                   | Статус |
|------------------|------------------------|--------|
| Mean Reversion   | `mean_reversion.py`    | ✅     |
| Breakout         | `breakout.py`          | ✅     |
| SMA              | `sma.py`               | ✅     |
| RSI              | `rsi.py`               | ✅     |
| Countertrend     | `countertrend.py`      | ✅     |
| SL/TP            | `sl_tp.py`             | ✅     |
| Adaptive         | `adaptive_strategy.py` | ✅     |

---

## 📂 Архитектура проекта

bot_ai/
├── backtest/       # Бэктестинг стратегий  
├── config/         # Загрузка параметров из JSON  
├── core/           # Логирование, утилиты  
├── diagnostics/    # Диагностика и отладка  
├── exec/           # Исполнение сделок (live/paper)  
├── filters/        # ATR/ADX фильтры входа  
├── risk/           # RiskManager, SL/TP, PositionSizer  
├── selector/       # Отбор и фильтрация пар  
├── state/          # Хранилище позиций и логгер сделок  
├── strategy/       # Реализация стратегий  
└── utils/          # Уведомления, вспомогательные функции

---

## ⚙️ Установка

git clone https://github.com/yourname/neurotrade.git  
cd neurotrade  
python -m venv .venv  
.venv\Scripts\activate  # Windows  
pip install -r requirements.txt

---

## ▶️ Примеры запуска

# Бэктест всех пар  
python night_backtest.py

# Live / Paper режим  
python bot_live.py

# Walk-Forward анализ (поэтапная переоценка стратегии)  
python walk_forward.py

# Grid-оптимизация параметров SMA/RSI  
python optimize_cli.py --symbol BTCUSDT --sma-fast 5,10,15 --sma-slow 30,40,50 --rsi 10,15

---

## 📊 Артефакты

- `results/grid_results.csv` — все комбинации параметров  
- `results/best_params.csv` — лучшие параметры по PnL  
- `results/heatmap_rsi_*.png` — тепловые карты  
- `logs/optimize_YYYYMMDD_HHMM.log` — логи оптимизации  
- `trades_log.csv`, `risk_blocks.csv` — сделки и блокировки

---

## 🧾 Пример конфигурации (`config.json`)

{
  "exchange": "binance",
  "mode": "paper",
  "capital": 10000,
  "risk_per_trade": 0.01,
  "min_risk_reward_ratio": 1.5,
  "stop_loss_pct": 0.02,
  "trailing_stop_pct": 0.015,
  "atr_threshold": 0.01,
  "atr_period": 14,
  "adx_threshold": 20,
  "adx_period": 14,
  "max_holding_period": 48
}

---

## 🧪 Тестирование

# Запуск всех тестов  
pytest -v

> Покрытие: **100%**  
> Тесты: `tests/test_*.py`

---

## 🔄 CI/CD

- GitHub Actions: прогон тестов, публикация артефактов  
- Makefile (в разработке): `make optimize`, `make test`, `make report`  
- Артефакты: PNG, CSV, JSON, equity-кривые  
- `run_tests.ps1`: локальный запуск всех тестов

---

## 📜 Документация

- `PROJECT_INFO.md` — паспорт проекта  
- `TODO.md` — архитектура селектора пар  
- `changes.log` — история изменений

---

## 📌 Статус

**Версия:** `0.4`  
**Этап:** `stage0.5_strategies_integration`  
**Дата:** _январь 2026_
