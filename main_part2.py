def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["backtest", "live", "paper"], required=True)
    parser.add_argument("--symbol")
    parser.add_argument("--strategy", required=True)
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--balance", type=float, default=1000)
    parser.add_argument("--config", default="config.json")
    args = parser.parse_args()

    print(f"🚀 Mode: {args.mode} | Strategy: {args.strategy} | Timeframe: {args.timeframe}")
    config = load_config(args.config)
    params = config.get("params", {})
    params["symbol"] = args.symbol

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    client = Client(api_key, api_secret)

    if args.mode == "live" and not args.symbol:
        symbols = filter_symbols(client, config)
        print(f"✅ Filtered symbols: {symbols}")
        return

    if not args.symbol:
        print("❌ Symbol is required for backtest/live/paper mode.")
        return

    if args.strategy == "breakout":
        strategy = BreakoutStrategy({"params": params})
    elif args.strategy == "mean_reversion":
        strategy = MeanReversionStrategy(params)
    elif args.strategy == "rsi":
        strategy = RSIReversalStrategy(params)
    else:
        print(f"❌ Unknown strategy: {args.strategy}")
        return

    if args.mode == "backtest":
        df_path = f"data/{args.symbol}_{args.timeframe}.csv"
        if not os.path.exists(df_path):
            print(f"❌ Data not found: {df_path}")
            return
        df = pd.read_csv(df_path)
        df["time"] = pd.to_datetime(df["time"])
        df = strategy.calculate_indicators(df)
        df = strategy.generate_signals(df)
        strategy.backtest(df, initial_balance=args.balance)
        summary_df = strategy.summary(args.symbol)
        metrics = calculate_metrics(summary_df, initial_balance=args.balance)

        if summary_df.empty:
            print("❌ No trades found.")
            return

        metrics_df = pd.DataFrame([{
            "symbol": args.symbol,
            "total_trades": metrics["trades"],
            "final_balance": metrics["final_balance"],
            "win_rate": metrics["win_rate"]
        }])

        os.makedirs("logs", exist_ok=True)
        metrics_df.to_csv("logs/top10.csv", index=False)

        for k, v in metrics.items():
            print(f"{k:>20}: {v}")

        top10_path = Path("logs/top10.csv")
        if top10_path.exists():
            df_top = pd.read_csv(top10_path)
            total_trades = df_top["total_trades"].sum()
            total_profit = df_top["final_balance"].sum()
            avg_winrate = df_top["win_rate"].mean()
            print("\n=== FINAL REPORT ===")
            print(f"📊 Total Trades: {total_trades}")
            print(f"💰 Total Final Balance: {total_profit:.2f}")
            print(f"🏆 Average Win Rate: {avg_winrate:.2f}%")
        else:
            print("❌ No top10.csv found. Backtest may have failed.")
        return

    elif args.mode == "paper":
        run_live(strategy, args.symbol, args.timeframe, client, initial_balance=args.balance, paper_mode=True)
        return

    elif args.mode == "live":
        run_live(strategy, args.symbol, args.timeframe, client, initial_balance=args.balance)
        return

    return

if __name__ == "__main__":
    main()
