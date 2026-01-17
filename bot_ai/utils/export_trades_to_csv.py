# ============================================
# 📤 export_trades_to_csv.py — Экспорт сделок
# --------------------------------------------
# Функция:
# - Сохраняет список сделок в CSV-файл
# - Автоматически создаёт директорию, если нужно
# - Поддерживает timestamp в имени файла
# Зависимости: pandas, os, datetime
# ============================================

import pandas as pd
import os
from datetime import datetime

def export_trades_to_csv(trades: list, output_dir: str = "exports", filename: str = None):
    """
    Экспортирует сделки в CSV

    Параметры:
    - trades: список словарей (entry, exit, sl, tp, direction и т.д.)
    - output_dir: папка для сохранения (по умолчанию: exports)
    - filename: имя файла (если None — генерируется с timestamp)

    Возвращает:
    - Полный путь к сохранённому файлу
    """
    if not trades:
        print("[export] Нет сделок для экспорта.")
        return None

    os.makedirs(output_dir, exist_ok=True)

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"trades_{timestamp}.csv"

    path = os.path.join(output_dir, filename)
    df = pd.DataFrame(trades)
    df.to_csv(path, index=False)

    print(f"[export] Сделки сохранены в: {path}")
    return path
