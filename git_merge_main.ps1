# ============================================
# 🔁 stash → merge → push → unstash
# ============================================

# 1. Убираем все изменения, включая отслеживаемые и неотслеживаемые
git stash push --include-untracked --all

# 2. Переключаемся на ветку main
git checkout main

# 3. Сливаем stage0.4_main_release
git merge stage0.4_main_release

# 4. Пушим в origin/main
git push origin main

# 5. Возвращаем stash обратно
git stash pop
