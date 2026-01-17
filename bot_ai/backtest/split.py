# ============================================
# 🧪 split.py — Train/Test разделение
# --------------------------------------------
# Функция:
# - Делит DataFrame на train/test
# - Поддерживает test_size (доля или int)
# - shuffle=False по умолчанию (для временных рядов)
# Зависимости: pandas
# ============================================

import pandas as pd
from typing import Tuple, Union

def train_test_split(
    df: pd.DataFrame,
    test_size: Union[float, int] = 0.2,
    shuffle: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Делит DataFrame на train и test

    Параметры:
    - df: исходный DataFrame
    - test_size: доля (0.2) или количество (int)
    - shuffle: перемешивать ли строки (по умолчанию False)

    Возвращает:
    - (train_df, test_df)
    """
    if df is None or df.empty:
        return df, pd.DataFrame()

    if isinstance(test_size, float):
        test_len = int(len(df) * test_size)
    else:
        test_len = test_size

    if test_len >= len(df):
        return df, pd.DataFrame()

    if shuffle:
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    train_df = df.iloc[:-test_len].copy()
    test_df = df.iloc[-test_len:].copy()

    return train_df, test_df
