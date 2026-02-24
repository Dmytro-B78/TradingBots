# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/analytics/report_generator.py
# Purpose: Generate a clean English backtest report from metrics
# ============================================

def generate_report(metrics: dict) -> str:
    if not metrics:
        return "No trades were executed. No report available."

    lines = []
    lines.append(f"Total Trades: {metrics.get('total_trades', 0)}")
    lines.append(f"Winning Trades: {metrics.get('winning_trades', 0)}")
    lines.append(f"Losing Trades: {metrics.get('losing_trades', 0)}")
    lines.append(f"Win Rate: {metrics.get('win_rate', 0):.2%}")
    lines.append(f"Average PnL: {metrics.get('average_pnl', 0):.4f}")
    lines.append(f"Total Return: {metrics.get('total_return', 0):.2%}")
    lines.append(f"Max Drawdown: {metrics.get('max_drawdown', 0):.2%}")
    lines.append(f"Profit Factor: {metrics.get('profit_factor', 0):.2f}")
    lines.append(f"Sharpe Ratio: {metrics.get('sharpe_ratio', 0):.2f}")
    lines.append(f"Final Capital: ${metrics.get('final_capital', 0):,.2f}")

    return "\n".join(lines)
