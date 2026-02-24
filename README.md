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

### 📋 План тестирования

#### TradeExecutor

| №  | Файл теста                        | Назначение                              | Статус |
|----|----------------------------------|------------------------------------------|--------|
| 1  | `test_comment.py`               | Генерация комментариев к сделке         | ✅     |
| 2  | `test_executor_logging.py`      | Логирование сделок в CSV                | ✅     |
| 3  | `test_executor_sl_tp.py`        | SL/TP и закрытие позиции                | ✅     |
| 4  | `test_executor_with_riskguard.py` | Проверка RiskGuard                     | ✅     |
| 5  | `test_executor_integration.py`  | Интеграция с внешними компонентами     | ✅     |
| 6  | `test_executor_errors.py`       | Обработка исключений и валидация       | ✅     |
| 7  | `test_executor_position.py`     | Управление активной позицией           | ✅     |
| 8  | `test_executor_equity.py`       | Ограничения по equity                  | ✅     |

#### Strategy

| №  | Файл теста               | Назначение                                      | Статус |
|----|--------------------------|--------------------------------------------------|--------|
| 9  | `test_strategy_basic.py` | Проверка базовой логики стратегии               | ⏳     |
| 10 | `test_strategy_filters.py` | Проверка фильтров (объём, RSI, спред и т.д.)    | ⏳     |
| 11 | `test_strategy_risk.py`   | Проверка взаимодействия стратегии с RiskGuard   | ⏳     |
| 12 | `test_strategy_live.py`   | Интеграция стратегии с TradeExecutor            | ⏳     |

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
---

## 🧠 Полный список стратегий

| Категория                | Название               | Файл                        | Логика                                                                 |
|--------------------------|------------------------|-----------------------------|------------------------------------------------------------------------|
| 📊 Индикаторы            | RSI                    | `rsi.py`                    | RSI < 30 → покупка, RSI > 70 → продажа                                |
|                          | RSI Reversal           | `rsi_reversal_strategy.py`  | Выход RSI из зон перекупленности/перепроданности                     |
|                          | RSI + MACD             | `rsi_macd.py`               | Рост RSI + MACD > 0 → покупка                                         |
|                          | RSI + Ichimoku         | `rsi_ichimoku.py`           | Рост RSI + Tenkan > Kijun → покупка                                   |
|                          | RSI + BBands           | `rsi_bbands.py`             | Цена ниже нижней BB → покупка                                         |
| 📉 Контртренд            | Countertrend           | `countertrend.py`           | RSI < 30 → покупка (разворот против тренда)                           |
|                          | Mean Reversion         | `mean_reversion.py`         | Цена сильно ниже MA (z-score) → покупка                               |
| 📈 Тренд / Пробой         | Breakout               | `breakout.py`               | Пробой максимума за N свечей → покупка                                |
|                          | Volatile               | `volatile.py`               | Волатильность (std high) > порога → покупка                           |
| 📊 Скользящие средние    | SMA                    | `sma.py`                    | Пересечение SMA_fast и SMA_slow                                       |
|                          | MA Crossover           | `ma_crossover_strategy.py`  | Fast MA пересекает Slow MA                                            |
|                          | Simple MA              | `simple_ma.py`              | Цена пересекает MA                                                    |
| 🛡 Управление рисками     | SL/TP                  | `sl_tp.py`                  | Цена ↑ > TP% → продажа, ↓ > SL% → покупка                             |
| 🧪 Для бэктеста           | RSI (backtest)         | `rsi_for_backtest.py`       | Универсальная RSI-логика для live и backtest                          |
|                          | SMA (backtest)         | `sma_for_backtest.py`       | Универсальная SMA-логика для live и backtest                          |

## 🧠 Сравнение стратегий

Модуль \compare_runner.py\ позволяет запускать автоматическое сравнение нескольких стратегий на выбранных торговых парах с анализом метрик и визуализацией результатов.

### 🔧 Настройка

Добавьте в \config.json\:

\\\json
"compare": {
  "strategies": ["breakout", "mean_reversion"]
},
"strategy_params": {
  "breakout": { "window": 10 },
  "mean_reversion": { "sma_fast": 10, "sma_slow": 30, "rsi_period": 14 }
}
\\\

### ▶️ Запуск

\\\ash
python compare_runner.py --config config.json
\\\

### 📤 Артефакты

- \esults/compare_summary.csv\ — таблица метрик по стратегиям и парам  
- \esults/compare_plot.png\ — график доходности по стратегиям  
- \logs/compare.log\ — лог-файл с результатами и ошибками
## 🧠 Адаптивный выбор стратегии

Модуль `strategy_router.py` автоматически анализирует рыночные условия и подбирает наиболее подходящую стратегию из каталога.

### 🔍 Анализ рынка

Функция `classify_market_conditions(df)` вычисляет:

- **Волатильность**: стандартное отклонение доходности
- **Тренд**: направление движения цены (вверх / вниз / флэт)
- **RSI**: индекс относительной силы
- **Объём**: средний объём за последние свечи

### 🧩 Подбор стратегии

Функция `match_strategy(market_conditions)`:

- Сопоставляет текущие рыночные условия с критериями из `strategy_catalog.py`
- Возвращает имя стратегии, соответствующей условиям (например, `mean_reversion`, `breakout`)

### ⚙️ Инициализация стратегии

Функция `route_strategy(df, config)`:

- Вызывает `classify_market_conditions`
- Подбирает стратегию через `match_strategy`
- Загружает класс стратегии и её параметры
- Возвращает готовый экземпляр стратегии

### 📚 Каталог стратегий

Файл `strategy_catalog.py` содержит:

- Названия и описания стратегий
- Условия применения (волатильность, тренд, RSI и т.д.)
- Параметры и их значения по умолчанию
- Сетки параметров для оптимизации

