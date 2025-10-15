import os
import shutil
import pytest

# ============================
# conftest.py для тестов NT
# ============================
# - Гарантирует наличие whitelist.json в temp
# - Исправляет путь назначения (без пробелов)
# - Использует os.path.join для кроссплатформенности
# ============================

@pytest.fixture(autouse=True)
def prepare_whitelist(tmp_path):
    """
    Автоматическая фикстура:
    - Создаёт копию data/whitelist.json в temp
    - Обеспечивает корректный путь без пробелов
    """
    # Путь к исходному whitelist.json
    src_file = os.path.join("data", "whitelist.json")

    # Путь к временному whitelist.json
    dst_file = os.path.join(tmp_path, "whitelist_test.json")

    # Если исходного файла нет — создаём пустой
    if not os.path.exists(src_file):
        os.makedirs("data", exist_ok=True)
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("{}")

    # Копируем whitelist.json во временную папку
    shutil.copyfile(src_file, dst_file)

    # Возвращаем путь для тестов
    return dst_file
