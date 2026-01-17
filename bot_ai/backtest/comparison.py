import logging
import os
from datetime import datetime, timedelta

import pandas as pd

def compare_strategies(backtests_dir='data/backtests', days=7):
    logger = logging.getLogger(__name__)
    if not os.path.exists(backtests_dir):
        logger.warning("Папка с backtest не найдена.")
        return

    cutoff_time = datetime.utcnow() - timedelta(days=days)
    summaries = []

    # Ищем summary.csv за последние N дней
    for root, dirs, files in os.walk(backtests_dir):
        for file in files:
            if file == 'summary.csv':
                try:
                    folder_time_str = os.path.basename(root).split('_')[-1]
                    # Пытаемся распарсить дату из имени папки
                    folder_datetime = datetime.strptime(
                        folder_time_str, "%Y%m%d") if len(folder_time_str) == 8 else None
                except Exception:
                    folder_datetime = None

                if folder_datetime and folder_datetime >= cutoff_time:
                    strategy_name = os.path.basename(root).split('_')[0]
                    df = pd.read_csv(os.path.join(root, file))
                    df['Strategy'] = strategy_name
                    df['TestDate'] = folder_datetime
                    summaries.append(df)

    if not summaries:
        logger.warning(f"Не найдено тестов за последние {days} дней.")
        return

    all_results = pd.concat(summaries, ignore_index=True)

    # Средняя прибыль по стратегиям за период
    avg_profit = all_results.groupby(
        'Strategy')['TotalProfit(%)'].mean().reset_index()

    # Лучшая и худшая пара по каждой стратегии
    best_pairs = all_results.loc[all_results.groupby(
        'Strategy')['TotalProfit(%)'].idxmax()]
    worst_pairs = all_results.loc[all_results.groupby(
        'Strategy')['TotalProfit(%)'].idxmin()]

    logger.info(f"=== Средняя прибыль по стратегиям за {days} дней ===")
    for _, row in avg_profit.iterrows():
        logger.info(f"{row['Strategy']}: {row['TotalProfit(%)']:.2f}%")

    logger.info("=== Лучшая пара по стратегиям ===")
    for _, row in best_pairs.iterrows():
        logger.info(
            f"{row['Strategy']}: {row['Symbol']} ({row['TotalProfit(%)']:.2f}%)")

    logger.info("=== Худшая пара по стратегиям ===")
    for _, row in worst_pairs.iterrows():
        logger.info(
            f"{row['Strategy']}: {row['Symbol']} ({row['TotalProfit(%)']:.2f}%)")

    # Сохраняем полный отчёт
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M")
    comparison_file = os.path.join(backtests_dir, f"comparison_{ts}.csv")
    all_results.to_csv(comparison_file, index=False)
    logger.info(f"Сравнительный отчёт сохранён в {comparison_file}")

