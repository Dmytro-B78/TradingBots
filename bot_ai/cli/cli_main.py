# -*- coding: utf-8 -*-
# ============================================
# File: bot_ai/cli/cli_main.py
# Назначение: CLI-роутер для запуска режимов live, paper, backtest, monitor
# ============================================

import argparse
import sys

def run_live():
    from bot_ai.core.bot_live import main as live_main
    live_main()

def run_paper():
    from bot_ai.core.bot_paper import main as paper_main
    paper_main()

def run_backtest(capital, risk_pct):
    from bot_ai.backtest.backtest_runner import main as backtest_main
    backtest_main(capital=capital, risk_pct=risk_pct)

def run_monitor():
    from bot_ai.diagnostics.monitor_main import main as monitor_main
    monitor_main()

def main():
    parser = argparse.ArgumentParser(description="🚀 AI Trading CLI — запуск торговых режимов")
    parser.add_argument(
        "mode",
        choices=["live", "paper", "backtest", "monitor"],
        help="Выберите режим: live (реальная торговля), paper (бумажная торговля), backtest (бэктест), monitor (мониторинг)"
    )
    parser.add_argument("--capital", type=float, default=10000, help="Начальный капитал для бэктеста")
    parser.add_argument("--risk", type=float, default=0.01, help="Риск на сделку (доля от капитала)")

    args = parser.parse_args()

    if args.mode == "live":
        run_live()
    elif args.mode == "paper":
        run_paper()
    elif args.mode == "backtest":
        run_backtest(capital=args.capital, risk_pct=args.risk)
    elif args.mode == "monitor":
        run_monitor()
    else:
        print("❌ Неизвестный режим. Используйте: live, paper, backtest или monitor.")
        sys.exit(1)

if __name__ == "__main__":
    main()
