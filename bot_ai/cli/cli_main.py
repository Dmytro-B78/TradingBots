# cli_main.py
# Назначение: CLI-интерфейс для запуска стратегий, бэктеста, мониторинга
# Структура:
# └── bot_ai/cli/cli_main.py

import argparse
import sys

def run_live():
    from bot_ai.core.bot_live import main as live_main
    live_main()

def run_paper():
    from bot_ai.core.bot_paper import main as paper_main
    paper_main()

def run_backtest():
    from bot_ai.backtest.backtest_runner import main as backtest_main
    backtest_main()

def run_monitor():
    from bot_ai.diagnostics.monitor_main import main as monitor_main
    monitor_main()

def main():
    parser = argparse.ArgumentParser(description="🤖 AI Trading CLI")
    parser.add_argument("mode", choices=["live", "paper", "backtest", "monitor"], help="Режим запуска")

    args = parser.parse_args()

    if args.mode == "live":
        run_live()
    elif args.mode == "paper":
        run_paper()
    elif args.mode == "backtest":
        run_backtest()
    elif args.mode == "monitor":
        run_monitor()
    else:
        print("❌ Неизвестный режим")
        sys.exit(1)

if __name__ == "__main__":
    main()
