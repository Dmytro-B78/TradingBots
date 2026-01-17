# ============================================
# 📦 Подготовка коммита и пуша для Pull Request
# Репозиторий: https://github.com/Dmytro-B78/TradingBots
# ============================================

# 1. Переключаемся на ветку stage0.4_main_release
git checkout stage0.4_main_release

# 2. Добавляем все изменения
git add .

# 3. Коммитим с сообщением
git commit -m "WIP: подготовка изменений для PR в main"

# 4. Пушим в origin
git push origin stage0.4_main_release

# 5. Открываем ссылку на создание Pull Request
Start-Process "https://github.com/Dmytro-B78/TradingBots/compare/main...stage0.4_main_release"
