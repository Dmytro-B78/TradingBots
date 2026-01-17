# -*- coding: utf-8 -*-
# ============================================
# File: cli.py
# Назначение: CLI-интерфейс с поддержкой --open-report и --output-dir
# ============================================

import argparse
import webbrowser
import os
from backtest.backtest_engine import run_backtest
from backtest.walk_forward import walk_forward_test
from bot_ai.utils.data import fetch_ohlcv

def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # === backtest ===
    parser_backtest = subparsers.add_parser("backtest", help="Запуск обычного бэктеста")
    parser_backtest.add_argument("--symbol", type=str, default="BTCUSDT", help="Торговая пара")
    parser_backtest.add_argument("--strategy", type=str, default="adaptive", help="Имя стратегии")
    parser_backtest.add_argument("--timeframe", type=str, default="1h", help="Таймфрейм")
    parser_backtest.add_argument("--open-report", action="store_true", help="Открыть HTML-отчёт после завершения")
    parser_backtest.add_argument("--output-dir", type=str, default=".", help="Папка для сохранения отчётов")

    # === walk-forward ===
    parser_wf = subparsers.add_parser("walk-forward", help="Walk-forward анализ")
    parser_wf.add_argument("--symbol", type=str, default="BTCUSDT", help="Торговая пара")
    parser_wf.add_argument("--strategy", type=str, default="adaptive", help="Имя стратегии")
    parser_wf.add_argument("--timeframe", type=str, default="1h", help="Таймфрейм")
    parser_wf.add_argument("--window", type=int, default=100, help="Размер окна")
    parser_wf.add_argument("--step", type=int, default=20, help="Шаг окна")
    parser_wf.add_argument("--open-report", action="store_true", help="Открыть HTML-отчёт после завершения")
    parser_wf.add_argument("--output-dir", type=str, default=".", help="Папка для сохранения отчётов")

    args = parser.parse_args()

    config = {
        "strategy": args.strategy,
        "symbol": args.symbol,
        "timeframe": args.timeframe,
        "output_dir": args.output_dir
    }

    os.makedirs(args.output_dir, exist_ok=True)

    if args.command == "backtest":
        run_backtest(args.symbol, args.strategy, args.timeframe, config)
        if args.open_report:
            webbrowser.open(os.path.join(args.output_dir, "backtest_report.html"))

    elif args.command == "walk-forward":
        df = fetch_ohlcv(args.symbol, args.timeframe)
        if df is None or df.empty:
            print("❌ Нет данных")
            return
        walk_forward_test(df, args.strategy, config, window_size=args.window, step_size=args.step)
        if args.open_report:
            webbrowser.open(os.path.join(args.output_dir, "backtest_report.html"))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
