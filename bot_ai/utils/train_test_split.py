# bot_ai/utils/train_test_split.py

import pandas as pd

def split_by_time(df: pd.DataFrame, train_ratio: float = 0.7):
    """
    Делит DataFrame по времени: первые N% — train, оставшиеся — test.
    """
    df = df.sort_values("time").reset_index(drop=True)
    split_index = int(len(df) * train_ratio)
    train = df.iloc[:split_index].copy()
    test = df.iloc[split_index:].copy()
    return train, test
