# -*- coding: utf-8 -*-
# === bot_ai/analytics/equity_report.py ===
# Генерация PDF-отчёта с фильтрацией и группировкой

import argparse
import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def load_data(csv_path):
    if not os.path.exists(csv_path):
        print(f"Файл {csv_path} не найден.")
        return None
    try:
        df = pd.read_csv(csv_path, parse_dates=["closed_at"])
        return df
    except Exception as e:
        print(f"Ошибка загрузки CSV: {e}")
        return None

def filter_data(df, strategy=None, symbol=None, date_from=None, date_to=None):
    if strategy:
        df = df[df["strategy"] == strategy]
    if symbol:
        df = df[df["symbol"] == symbol]
    if date_from:
        df = df[df["closed_at"] >= pd.to_datetime(date_from)]
    if date_to:
        df = df[df["closed_at"] <= pd.to_datetime(date_to)]
    return df.sort_values("closed_at")

def calculate_equity(df, initial_balance=1000):
    balance = [initial_balance]
    for pnl in df["pnl_usdt"]:
        balance.append(balance[-1] + pnl)
    df["balance"] = balance[1:]
    return df

def plot_equity(df, ax):
    ax.plot(df["closed_at"], df["balance"], color="blue", linewidth=2)
    ax.set_title("Equity Curve")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Баланс (USDT)")
    ax.grid(True)

def plot_histogram(df, ax):
    ax.hist(df["pnl_usdt"], bins=20, color="green", edgecolor="black")
    ax.set_title("Распределение прибыли/убытков")
    ax.set_xlabel("PnL (USDT)")
    ax.set_ylabel("Количество сделок")
    ax.grid(True)

def plot_grouped(df, group_by, ax):
    if group_by == "week":
        df["period"] = df["closed_at"].dt.to_period(
            "W").apply(lambda r: r.start_time)
    elif group_by == "month":
        df["period"] = df["closed_at"].dt.to_period(
            "M").apply(lambda r: r.start_time)
    else:
        return

    grouped = df.groupby("period")["pnl_usdt"].sum().cumsum()
    ax.plot(grouped.index, grouped.values, marker="o", color="purple")
    ax.set_title(f"Equity по {group_by}")
    ax.set_xlabel("Период")
    ax.set_ylabel("Баланс (USDT)")
    ax.grid(True)

def generate_pdf(df, group_by, output="report.pdf"):
    with PdfPages(output) as pdf:
        fig, axs = plt.subplots(3, 1, figsize=(10, 12))
        plot_equity(df, axs[0])
        plot_histogram(df, axs[1])
        plot_grouped(df, group_by, axs[2])
        plt.tight_layout()
        pdf.savefig(fig)
        plt.close()
    print(f"? Отчёт сохранён в {output}")

def main():
    parser = argparse.ArgumentParser(
        description="Генерация PDF-отчёта по сделкам")
    parser.add_argument(
        "--csv",
        default="trades_log.csv",
        help="Путь к CSV-файлу")
    parser.add_argument("--strategy", help="Фильтр по стратегии")
    parser.add_argument("--symbol", help="Фильтр по символу")
    parser.add_argument(
        "--from",
        dest="date_from",
        help="Фильтр: дата от (YYYY-MM-DD)")
    parser.add_argument(
        "--to",
        dest="date_to",
        help="Фильтр: дата до (YYYY-MM-DD)")
    parser.add_argument(
        "--group",
        choices=[
            "week",
            "month"],
        default="month",
        help="Группировка по времени")
    parser.add_argument(
        "--balance",
        type=float,
        default=1000,
        help="Начальный баланс")
    parser.add_argument(
        "--output",
        default="report.pdf",
        help="Имя выходного PDF-файла")

    args = parser.parse_args()
    df = load_data(args.csv)
    if df is None or df.empty:
        print("Нет данных для анализа.")
        return

    df = filter_data(
        df,
        args.strategy,
        args.symbol,
        args.date_from,
        args.date_to)
    if df.empty:
        print("Фильтр вернул пустой результат.")
        return

    df = calculate_equity(df, args.balance)
    generate_pdf(df, args.group, args.output)

if __name__ == "__main__":
    main()

