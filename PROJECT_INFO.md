# PROJECT_INFO.md

## 1. Общая информация
NeuroTrade (NT) — модульный торговый бот с поддержкой CI/CD, строгим контролем рисков и прозрачной диагностикой.  
Цель — построить автономного торгового агента, способного адаптироваться к рыночным условиям, выбирать стратегии и пары, управлять рисками и вести отчётность.

## 2. Архитектура

- **bot_ai/** — ядро бота: стратегии, селектор, фильтры
- **risk/** — RiskGuard: контроль рисков, блокировки
- **exec/** — TradeExecutor: исполнение сделок
- **selector/** — выбор торговых пар и стратегий
- **strategy/** — стратегии (SMA, RSI, SL/TP, adaptive)
- **state/** — позиции, баланс, история (в разработке)
- **backtest/** — симуляции, Train/Test, Walk-forward
- **diagnostics/** — визуализации, отчёты, логи
- **tests/** — тесты всех модулей
- **config/** — параметры стратегий, профили, лимиты

## 3. CI/CD

- Все тесты запускаются через `run_tests.ps1`
- GitHub Actions: прогон тестов, публикация отчётов
- Артефакты: `trades_log.csv`, `risk_blocks.csv`, equity-кривые
- Makefile (в разработке) для установки зависимостей и генерации отчётов

## 4. Компоненты

### 4.1 Selector
- `pipeline.py`: оркестратор отбора пар и стратегий
- `filters.py`: атомарные фильтры (объём, спред, тренд, риск)
- `trend_utils.py`: проверка тренда через SMA
- Планируется: интеграция `strategy_chooser`, классификация рынка

### 4.2 RiskGuard
- Контроль лимитов: размер позиции, дневной убыток, общее количество сделок
- Блокировки логируются в `risk_blocks.csv`
- Интеграция с TradeExecutor

### 4.3 TradeExecutor
- Исполнение сигналов в режиме `paper` и `live`
- Логирование сделок в `trades_log.csv`
- Поддержка RiskGuard

### 4.4 Strategy
- Поддержка `mode: backtest / paper / live`
- Поддержка `max_holding_period`, `min_risk_reward_ratio`, `side=0`
- Фильтры: ATR, ADX, тренд
- В разработке: мульти-таймфрейм фильтр, профили под режимы рынка

## 5. Этапы проекта

### ✅ Stage 0.4 Main Release
- RiskGuard стабилен, TradeExecutor интегрирован
- Прогон в режиме `paper`, сохранены логи
- Ветка `stage0.4_main_release` зафиксирована

### 🔄 Stage 0.5 Strategies Integration (в процессе)
- Подключение стратегий (SMA, RSI, SL/TP)
- Расширение тестов
- Визуализация сигналов
- Подготовка к `pre_live`


C:\TradingBots\NT
├── walk_forward.py                  # 🔁 Основной скрипт walk-forward
├── run_backtest_once.py            # 🧪 Ручной запуск бэктеста (ранее backtest.py)
├── data\
│   └── BTCUSDT_1h.csv              # 📊 Исторические данные
├── results\
│   └── walk_forward\               # 💾 Результаты оптимизации
│       └── walk_forward_results.json
├── bot_ai\
│   ├── __init__.py
│   ├── optimize.py                 # ⚙️ Grid-оптимизация (run_grid_optimization)
│   ├── config\
│   │   └── config_loader.py        # ⚙️ Загрузка конфигурации
│   ├── strategy\
│   │   └── mean_reversion.py       # 📈 Стратегия Mean Reversion
│   ├── backtest\
│   │   ├── __init__.py             # ← содержит: from .backtest import run_backtest
│   │   └── backtest.py             # 🧪 run_backtest
│   └── utils\
│       └── notifier.py             # 📲 Telegram Notifier
