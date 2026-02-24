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
#### 4.1.1 pipeline.py — отбор пар

- **`select_pairs(cfg)`**  
  Отбирает пары по объёму, спреду, тренду и стратегии.  
  Возвращает список словарей:  
  `[{"pair": "BTC/USDT", "regime": "uptrend", "strategy": "adaptive"}, ...]`

- **`fetch_and_filter_pairs(cfg, use_cache=True, cache_ttl_hours=24)`**  
  Загружает whitelist из кэша или вызывает `select_pairs()`.  
  Возвращает список строк:  
  `["BTC/USDT", "ETH/USDT"]`

- **`show_top_pairs(cfg, pairs)`**  
  Логирует объёмы по парам через `ccxt.fetch_ticker()`.

- ✅ Покрыто юнит‑тестами:
  - `test_select_pairs_no_cache`
  - `test_select_pairs_with_cache`
  - `test_show_top_pairs_logs_volume`
  - `test_pipeline_end_to_end`

- `pipeline.py`: оркестратор отбора пар и стратегий  
- `filters.py`: атомарные фильтры (объём, спред, тренд, риск)  
- `trend_utils.py`: проверка тренда через SMA  
- Планируется: интеграция `strategy_chooser`, классификация рынка  

### 4.2 RiskGuard
#### 4.2.1 risk_guard.py — контроль рисков

- **check_limits(position, trade, cfg)**  
  Проверяет, не превышает ли сделка лимиты по объёму, проценту от баланса, дневному убытку и количеству сделок.  
  Возвращает True, если всё в пределах допустимого, иначе False.

- **should_block_trade(pair, reason)**  
  Проверяет, заблокирована ли пара по причине (olume, spread, loss_limit, cooldown).  
  Возвращает True, если торговля запрещена.

- **log_block_event(pair, reason, details)**  
  Записывает событие блокировки в isk_blocks.csv с причиной и параметрами.

- **load_risk_config(cfg)**  
  Загружает параметры лимитов из конфигурации:  
  max_per_trade_usdt, max_per_trade_pct, daily_loss_limit_usdt, max_spread_pct, cooldown_minutes.

- ✅ Покрыто юнит‑тестами:
  - 	est_risk_guard_limits
  - 	est_blocking_logic
  - 	est_log_block_event
  - 	est_risk_guard_integration

- Планируется:
  - Поддержка динамических лимитов на основе волатильности  
  - Интеграция с Telegram-уведомлениями при блокировках  
  - Поддержка исключений по whitelist/blacklist
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

## 6. Параметры по умолчанию

- `max_per_trade_usdt`: 25  
- `max_per_trade_pct`: 0.5  
- `daily_loss_limit_usdt`: 15  
- `max_spread_pct`: 0.08  
- `min_24h_volume_usdt`: 20_000_000  

### Уведомления
- `enabled`: false  
- `provider`: telegram  
- `telegram_token`: ""  
- `telegram_chat_id`: ""  

## 7. Тесты и покрытие

- `test_pipeline_end_to_end` — проверка полного цикла отбора пар  
- `test_risk_guard_limits` — проверка лимитов RiskGuard  
- `test_executor_logging` — проверка логирования сделок  
- `test_strategy_filters` — валидация фильтров ATR, ADX, тренда  
- `test_project_state_snapshot` — фиксация состояния проекта  

Покрытие: ~85% модулей покрыто юнит‑тестами  

## 8. TODO / Roadmap

- [x] Интеграция RiskGuard с TradeExecutor  
- [x] CI/CD: GitHub Actions + отчёты  
- [ ] Интеграция стратегий SMA, RSI, SL/TP  
- [ ] Визуализация сигналов  
- [ ] Поддержка мульти-таймфрейм фильтров  
- [ ] Telegram-уведомления  
- [ ] Поддержка профилей под режимы рынка  
- [ ] Подключение real-time данных через WebSocket  

## 9. История версий

### v0.4 — 2026‑02‑02
- Добавлен блок `4.1.1 pipeline.py`  
- Обновлён раздел «📌 Состояние проекта»  
- Удалены Git-конфликты, файл сохранён в UTF-8 без BOM  

### v0.3 — 2025‑09‑18
- Интеграция RiskGuard  
- CI/CD пайплайн  
- Логирование сделок  

## 📌 Состояние проекта — 2026‑02‑02 01:25

- **Версия проекта:** 0.4  
- **Последнее обновление паспорта:** 2026‑02‑02  
- **Результат тестов:** 4 passed, 0 failed  
- **Артефакты snapshot:** project_snapshot.txt, TradingBots_backup_4.zip  

#### 🟢 Что работает
- Selector: отбор пар, кэш, логика тренда и стратегии  
- Все ключевые функции покрыты тестами  
- CI/CD: `run_tests.ps1`, GitHub Actions  

#### 🔜 Следующий этап
- Перейти к модулю `risk_guard`  
- Проверить фильтрацию по лимитам и блокировкам  
- Написать тесты на `risk_guard.py`  
#### 4.2.1 risk_guard.py — контроль рисков

- **`check_limits(position, trade, cfg)`**  
  Проверяет, не превышает ли сделка лимиты по объёму, проценту от баланса, дневному убытку и количеству сделок.  
  Возвращает `True`, если всё в пределах допустимого, иначе `False`.

- **`should_block_trade(pair, reason)`**  
  Проверяет, заблокирована ли пара по причине (`volume`, `spread`, `loss_limit`, `cooldown`).  
  Возвращает `True`, если торговля запрещена.

- **`log_block_event(pair, reason, details)`**  
  Записывает событие блокировки в `risk_blocks.csv` с причиной и параметрами.

- **`load_risk_config(cfg)`**  
  Загружает параметры лимитов из конфигурации:  
  `max_per_trade_usdt`, `max_per_trade_pct`, `daily_loss_limit_usdt`, `max_spread_pct`, `cooldown_minutes`.

- ✅ Покрыто юнит‑тестами:
  - `test_risk_guard_limits`
  - `test_blocking_logic`
  - `test_log_block_event`
  - `test_risk_guard_integration`

- Планируется:
  - Поддержка динамических лимитов на основе волатильности  
  - Интеграция с Telegram-уведомлениями при блокировках  
  - Поддержка исключений по whitelist/blacklist  
