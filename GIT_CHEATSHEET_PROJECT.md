# 🚀 Git Cheat Sheet для проекта TradingBots

## 📌 Базовые команды
git status
git add .
git commit -m "Описание изменений"
git push origin main

## 🔄 Синхронизация с сервером
git pull origin main
git pull --rebase origin main
git push origin main

## 🛡️ Резервные копии
git checkout -b feature/riskguard-upgrade
git checkout main
git tag -a backup_stage1 -m "Завершён этап RiskGuard + Dashboard"
git push origin backup_stage1

## 🚑 Восстановление
git checkout -- путь/к/файлу.py
git reset --soft HEAD~1
git reset --hard HEAD~1

## 📂 Рекомендация для проекта
git add .
git commit -m "✅ Завершён этап: RiskGuard + Dashboard + Reports"
git tag -a stage1 -m "Stage 1 complete"
git push origin main --tags

---

## ❗ Типичные ошибки и решения

### Ошибка: error: failed to push some refs to 'origin'
Причина: в удалённом репозитории есть новые коммиты.  
Решение:
git pull --rebase origin main
git push origin main

### Ошибка: merge conflict
Причина: изменения в одном и том же файле локально и на сервере.  
Решение:
1. Открыть файл, найти строки с <<<<<<<, =======, >>>>>>>.
2. Оставить нужный вариант, удалить метки.
3. Сделать коммит:
   git add .
   git commit -m "Resolve merge conflict"
   git push origin main

### Ошибка: случайно удалил изменения
Если ещё не коммитил:
git checkout -- путь/к/файлу.py

Если уже коммитил:
git reset --hard HEAD~1

### Ошибка: нужно отменить последний коммит, но оставить изменения в коде
git reset --soft HEAD~1
