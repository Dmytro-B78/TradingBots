# -*- coding: utf-8 -*-
# ============================================
# File: tests/conftest.py
# Назначение: Общие фикстуры для тестов NT
# ============================================
# - Копирует файл whitelist.json во временную папку
# - Создаёт его, если отсутствует
# - Возвращает путь к копии для использования в тестах
# ============================================

import os
import shutil
import pytest

@pytest.fixture(autouse=True)
def prepare_whitelist(tmp_path):
    """
    Подготовка тестового окружения:
    - Копирует data/whitelist.json во временную директорию
    - Создаёт пустой файл, если он отсутствует
    """
    src_file = os.path.join("data", "whitelist.json")
    dst_file = os.path.join(tmp_path, "whitelist_test.json")

    if not os.path.exists(src_file):
        os.makedirs("data", exist_ok=True)
        with open(src_file, "w", encoding="utf-8") as f:
            f.write("{}")

    shutil.copyfile(src_file, dst_file)
    return dst_file
