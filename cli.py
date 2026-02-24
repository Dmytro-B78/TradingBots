# -*- coding: utf-8 -*-
# ============================================
# File: cli.py
# Р СњР В°Р В·Р Р…Р В°РЎвЂЎР ВµР Р…Р С‘Р Вµ: CLI-Р С‘Р Р…РЎвЂљР ВµРЎР‚РЎвЂћР ВµР в„–РЎРѓ РЎРѓ Р С—Р С•Р Т‘Р Т‘Р ВµРЎР‚Р В¶Р С”Р С•Р в„– --open-report Р С‘ --output-dir
# ============================================

import argparse
import webbrowser
import os
from backtest.backtest_engine import run_backtest
from backtest.walk_forward import walk_forward_test
from bot_ai.utils.data import fetch_ohlcv

def main():
    parser = argparse.ArgumentParser(description="Trading Bot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Р С™Р С•Р СР В°Р Р…Р Т‘РЎвЂ№")

    # === backtest ===
    parser_backtest = subparsers.add_parser("backtest", help="Р вЂ”Р В°Р С—РЎС“РЎРѓР С” Р С•Р В±РЎвЂ№РЎвЂЎР Р…Р С•Р С–Р С• Р В±РЎРЊР С”РЎвЂљР ВµРЎРѓРЎвЂљР В°")
    parser_backtest.add_argument("--symbol", type=str, default="BTCUSDT", help="Р СћР С•РЎР‚Р С–Р С•Р Р†Р В°РЎРЏ Р С—Р В°РЎР‚Р В°")
    parser_backtest.add_argument("--strategy", type=str, default="adaptive", help="Р ВР СРЎРЏ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘")
    parser_backtest.add_argument("--timeframe", type=str, default="1h", help="Р СћР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р С")
    parser_backtest.add_argument("--open-report", action="store_true", help="Р С›РЎвЂљР С”РЎР‚РЎвЂ№РЎвЂљРЎРЉ HTML-Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљ Р С—Р С•РЎРѓР В»Р Вµ Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р ВµР Р…Р С‘РЎРЏ")
    parser_backtest.add_argument("--output-dir", type=str, default=".", help="Р СџР В°Р С—Р С”Р В° Р Т‘Р В»РЎРЏ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…Р С‘РЎРЏ Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљР С•Р Р†")

    # === walk-forward ===
    parser_wf = subparsers.add_parser("walk-forward", help="Walk-forward Р В°Р Р…Р В°Р В»Р С‘Р В·")
    parser_wf.add_argument("--symbol", type=str, default="BTCUSDT", help="Р СћР С•РЎР‚Р С–Р С•Р Р†Р В°РЎРЏ Р С—Р В°РЎР‚Р В°")
    parser_wf.add_argument("--strategy", type=str, default="adaptive", help="Р ВР СРЎРЏ РЎРѓРЎвЂљРЎР‚Р В°РЎвЂљР ВµР С–Р С‘Р С‘")
    parser_wf.add_argument("--timeframe", type=str, default="1h", help="Р СћР В°Р в„–Р СРЎвЂћРЎР‚Р ВµР в„–Р С")
    parser_wf.add_argument("--window", type=int, default=100, help="Р В Р В°Р В·Р СР ВµРЎР‚ Р С•Р С”Р Р…Р В°")
    parser_wf.add_argument("--step", type=int, default=20, help="Р РЃР В°Р С– Р С•Р С”Р Р…Р В°")
    parser_wf.add_argument("--open-report", action="store_true", help="Р С›РЎвЂљР С”РЎР‚РЎвЂ№РЎвЂљРЎРЉ HTML-Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљ Р С—Р С•РЎРѓР В»Р Вµ Р В·Р В°Р Р†Р ВµРЎР‚РЎв‚¬Р ВµР Р…Р С‘РЎРЏ")
    parser_wf.add_argument("--output-dir", type=str, default=".", help="Р СџР В°Р С—Р С”Р В° Р Т‘Р В»РЎРЏ РЎРѓР С•РЎвЂ¦РЎР‚Р В°Р Р…Р ВµР Р…Р С‘РЎРЏ Р С•РЎвЂљРЎвЂЎРЎвЂРЎвЂљР С•Р Р†")

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
            print("РІСњРЉ Р СњР ВµРЎвЂљ Р Т‘Р В°Р Р…Р Р…РЎвЂ№РЎвЂ¦")
            return
        walk_forward_test(df, args.strategy, config, window_size=args.window, step_size=args.step)
        if args.open_report:
            webbrowser.open(os.path.join(args.output_dir, "backtest_report.html"))

    else:
        parser.print_help()

if __name__ == "__main__":
    main()

