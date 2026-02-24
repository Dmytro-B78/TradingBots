# executor.py — Исполнение сделок

Модуль `executor.py` отвечает за приём торговых сигналов, проверку условий и выставление ордеров в режиме `paper` или `live`.

---

## ⚙️ 1. Основные функции

### `execute_trade(signal, cfg, market_data)`

**Назначение:**  
Обрабатывает торговый сигнал: проверяет лимиты, вызывает RiskGuard, логирует сделку, отправляет ордер (или симулирует).

**Вход:**  
- `signal`: словарь с полями `pair`, `side`, `entry`, `sl`, `tp`, `confidence`  
- `cfg`: конфигурация исполнения  
- `market_data`: текущие цены и объёмы

**Поведение:**  
- Проверяет лимиты через `risk_guard.check_limits()`  
- Проверяет блокировки через `risk_guard.should_block_trade()`  
- В режиме `paper`: логирует сделку в `trades_log.csv`  
- В режиме `live`: вызывает `ccxt.create_order()`  
- Возвращает статус: `"executed"`, `"blocked"`, `"skipped"`

---

### `log_trade_to_csv(trade_dict)`

**Назначение:**  
Сохраняет информацию о сделке в `trades_log.csv`.

**Поля:**  
- `timestamp`, `pair`, `side`, `entry`, `sl`, `tp`, `confidence`, `mode`, `status`

**Особенности:**  
- Проверяет наличие заголовка  
- Создаёт файл, если не существует  
- Добавляет строку в конец

---

## 🧪 2. Покрытие тестами

- `test_execute_trade_paper_mode()` — симуляция сделки  
- `test_execute_trade_blocked_by_risk()` — проверка блокировки  
- `test_log_trade_to_csv_format()` — корректность логирования  
- `test_executor_risk_integration()` — связка с RiskGuard  
- `test_executor_invalid_signal()` — поведение при ошибке

---

## 🛠️ TODO

- [ ] Поддержка частичного исполнения  
- [ ] Обработка ошибок ccxt (rate limit, insufficient funds)  
- [ ] Поддержка `reduce_only`, `post_only`, `client_order_id`  
- [ ] Интеграция с notifier (Telegram / email)  
- [ ] Поддержка trailing stop  
- [ ] Поддержка отмены ордеров по времени или событию  
