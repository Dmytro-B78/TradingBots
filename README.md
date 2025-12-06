# TradingBots

AI‑адаптивный торговый бот с прозрачной архитектурой, строгим контролем рисков и системой уведомлений.

## 🚀 Возможности
- Автоматический отбор торговых пар (D1 + LTF)
- Динамические SL/TP с учётом волатильности
- RiskGuard: дневные лимиты, kill-switch, cooldown
- Централизованная система уведомлений (Telegram)
- Поддержка backtest и диагностики

## 📂 Архитектура проекта
- bot_ai/core — конфиг, логирование
- bot_ai/selector — отбор и фильтрация пар
  - pipeline.py — оркестратор
  - filters.py — атомарные фильтры (spread, volume, riskguard, trend)
  - trend_utils.py — проверка тренда через SMA
- bot_ai/risk — RiskGuard, SL/TP, PositionSizer
- bot_ai/exec — исполнение сделок
- bot_ai/utils — утилиты (Notifier, pipeline_utils)
- bot_ai/diagnostics — диагностика и тесты
- bot_ai/backtest — движок тестирования стратегий

## ⚙️ Установка
git clone https://github.com/yourname/neurotrade.git
cd neurotrade
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
pytest -v

## 📜 Документация
- PROJECT_INFO.md — паспорт проекта
- TODO.md — архитектура селектора пар
- changes.log — история изменений

## 📌 Статус
Версия: 0.3 (сентябрь 2025)
