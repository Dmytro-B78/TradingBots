<<<<<<< HEAD
=======
<<<<<<< Updated upstream
import json
from pathlib import Path
from typing import Any, Dict
=======
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
﻿# config_loader.py
# Назначение: Загрузка переменных окружения из .env
# Структура:
# └── bot_ai/core/config_loader.py
<<<<<<< HEAD
=======
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)

from dotenv import load_dotenv
import os

load_dotenv()

<<<<<<< HEAD
def get_env(key, default=None):
    return os.getenv(key, default)
=======
<<<<<<< Updated upstream
    def get(self, *keys, default=None):
        cur = self.data
        for k in keys:
            if not isinstance(cur, dict) or k not in cur:
                return default
            cur = cur[k]
        return cur
=======
def get_env(key, default=None):
    return os.getenv(key, default)
>>>>>>> Stashed changes
>>>>>>> 47a38855 (🔥 Финальный merge: stage0.4_main_release → main, конфликты решены)
