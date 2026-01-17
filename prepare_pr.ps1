# ============================================
# 📦 Подготовка коммита и пуша для Pull Request
# ============================================

# 1. Переключаемся на нужную ветку
git checkout stage0.4_main_release

# 2. Добавляем все изменения
git add .

# 3. Коммитим с сообщением
git commit -m "WIP: подготовка изменений для PR в main"

# 4. Пушим в origin
git push origin stage0.4_main_release

# 5. Открываем ссылку на создание Pull Request (замени на свой репозиторий)
Start-Process "https://github.com/YOUR_USERNAME/YOUR_REPO/compare/main...stage0.4_main_release"
