# -*- coding: utf-8 -*-
# ============================================
# File: backtest/html_report.py
# Назначение: Генерация HTML-отчёта по результатам бэктеста
# ============================================

import pandas as pd
import datetime
import os

def generate_html_report(trades: list, metrics: dict, filename: str = "backtest_report.html"):
    """
    Генерирует HTML-отчёт с таблицей сделок, блоком метрик и графиком equity curve
    """
    if not trades:
        print("❌ Нет сделок для отчёта")
        return

    df = pd.DataFrame(trades)
    df_html = df.to_html(index=False, classes="table", border=0)

    metrics_html = "".join([
        f"<li><b>{key.replace('_', ' ').capitalize()}</b>: {value}</li>"
        for key, value in metrics.items()
    ])

    equity_img = ""
    if os.path.exists("equity_curve.png"):
        equity_img = '<h2>📉 Equity Curve</h2><img src="equity_curve.png" width="800">'

    html = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Отчёт по стратегии</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #333; }}
            .table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            .table th, .table td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
            .table th {{ background-color: #f2f2f2; }}
            ul {{ list-style-type: none; padding: 0; }}
            li {{ margin-bottom: 6px; }}
        </style>
    </head>
    <body>
        <h1>📊 Отчёт по стратегии</h1>
        <p><b>Дата генерации:</b> {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <h2>📌 Метрики</h2>
        <ul>{metrics_html}</ul>
        {equity_img}
        <h2>📋 Сделки</h2>
        {df_html}
    </body>
    </html>
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"📄 HTML-отчёт сохранён: {filename}")
