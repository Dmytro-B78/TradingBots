# report_generator.py
# Назначение: Генерация текстового отчёта по результатам бэктеста
# Структура:
# └── bot_ai/analytics/report_generator.py

def generate_report(metrics):
    report = f"""
📊 Backtest Report
-------------------------
📌 Сделок: {metrics['total_trades']}
💰 Финальный баланс: ${metrics['final_balance']:.2f}
📈 Точек на equity curve: {len(metrics['equity_curve'])}
"""
    return report.strip()
