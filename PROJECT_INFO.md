<<<<<<< HEAD
﻿# PROJECT_INFO.md
=======
<<<<<<< Updated upstream
﻿# NeuroTrade (NT) — Паспорт проекта
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

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


<<<<<<< HEAD
=======
logs/           # Логи  
data/           # История, кэш, результаты backtest  
=======
﻿# PROJECT_INFO.md

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
>>>>>>> Stashed changes

## 3. CI/CD

<<<<<<< Updated upstream
## 7. Параметры по умолчанию
- max_per_trade_usdt: 25
- max_per_trade_pct: 0.5
- daily_loss_limit_usdt: 15
- max_spread_pct: 0.08
- min_24h_volume_usdt: 20_000_000
- notifications:
  - enabled: false
  - provider: telegram
  - telegram_token: ""
  - telegram_chat_id: ""
=======
- Все тесты запускаются через `run_tests.ps1`
- GitHub Actions: прогон тестов, публикация отчётов
- Артефакты: `trades_log.csv`, `risk_blocks.csv`, equity-кривые
- Makefile (в разработке) для установки зависимостей и генерации отчётов
>>>>>>> Stashed changes

## 4. Компоненты

<<<<<<< Updated upstream
### 2025‑09‑18
- Исправлен баг с повторным заголовком в `trades_log.csv` (метод `log_trade_to_csv` в `executor.py`).
- Все тесты пройдены успешно (`pytest -v` — 2/2 PASSED).
- Созданы резервные копии проекта:
  - `TradingBots_backup_1.zip` — перед обновлением паспорта.
  - `TradingBots_backup_2.zip` — после обновления паспорта.
- Дорожная карта обновлена до версии 0.4.

### 2025‑09‑18 — Добавлен тест состояния проекта
- Создан тест `tests/test_project_state.py`, который:
  - Сохраняет снимок текущего состояния проекта в файл `project_snapshot.txt`.
  - Фиксирует дату и время, версию проекта, последнее обновление из `PROJECT_INFO.md` и результат прогона тестов.
- **Когда запускать:** в конце каждой рабочей сессии перед созданием резервной копии.
- **Зачем:** чтобы при следующем открытии проекта сразу видеть, на чём остановились и что уже сделано.
- **Как запускать:**  
  ```powershell
  python -m pytest tests/test_project_state.py
### ### 📌 Состояние проекта — 2025‑09‑21 21:15

- **Версия проекта:** 0.3  
- **Последнее обновление паспорта:** 2025‑09‑18  
- **Результат тестов:** 10 passed, 1 failed  
- **Артефакты snapshot:** project_snapshot.txt, TradingBots_backup_3.zip  

#### 🟢 Что работает
- RiskGuard (лимиты, kill‑switch, cooldown).  
- Notifier (уведомления через Telegram).  
- TradeExecutor (логирование сделок).  

#### 🔴 Что требует внимания
- 1 упавший тест (см. pytest -v).  
- Требуется анализ и исправление до перехода к версии 0.4.  

#### 📂 Действия перед следующим этапом
1. Найти и исправить причину падения теста.  
2. Обновить PROJECT_INFO.md (раздел «Обновление»).  
3. Сделать новый snapshot после фикса.  
4. Зафиксировать Git‑тег `stage0.3_fix`.  
------ tests/test_smoke.py::test_smoke FAILED  - упал смок-тест                                                                                                                                                          [100%]
=======
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


>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
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
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
