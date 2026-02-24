"""
Фильтр по множественным таймфреймам: оставляет сигналы, соответствующие заданному тренду.
"""

import pandas as pd

def apply_mtf_filter(signal_df: pd.DataFrame, timeframe_data: dict[str, pd.DataFrame], config: dict) -> pd.DataFrame:
    if not config.get("enabled", False):
        return signal_df

    required_trend = config.get("required_trend", "up")
    tf = next(iter(timeframe_data))  # берём первый доступный таймфрейм
    tf_df = timeframe_data[tf]

    # Объединяем по timestamp и symbol
    merged = pd.merge(signal_df, tf_df, on=["timestamp", "symbol"], how="left")

    # Фильтруем по тренду
    filtered = merged[merged["trend"] == required_trend]

    return filtered[signal_df.columns]
