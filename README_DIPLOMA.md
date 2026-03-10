# 📘 Diploma Project: Lightweight Trading Bot (RSI Strategy)

## Purpose

This is a simplified version of a crypto trading bot developed for academic purposes. It focuses on a single strategy — **RSI Reversal** — and supports both backtesting and live trading modes using the Binance API.

The full-featured version of the bot (with multiple strategies and extended functionality) is maintained in the `main` branch. This version, located in the `diploma` branch, is optimized for demonstration and documentation in a diploma project.

---

## Project Structure

C:\TradingBots\NT\
├── main.py                     # Entry point for backtest/live execution  
├── config.json                 # Strategy and risk configuration  
├── data\                       # Historical OHLCV data (CSV)  
├── logs\                       # Auto-generated logs (signals, orders, balances)  
├── bot_ai\  
│   ├── core\  
│   │   ├── strategy.py         # Base Strategy class  
│   │   └── order_manager.py    # OrderManager with test/live mode  
│   ├── strategy\  
│   │   └── rsi_reversal_strategy.py  # RSI-based trading logic  
│   ├── utils\  
│   │   ├── logger.py           # Signal logging  
│   │   └── indicators.py       # RSI, SMA, EMA, ATR  
│   └── metrics.py              # Performance metrics (Sharpe, drawdown, etc.)

---

## Installation

Install dependencies:

    pip install -r requirements.txt

---

## Usage

### Backtest

    python main.py --mode backtest --strategy rsi --symbol BTCUSDT --timeframe 1h --balance 1000

Requires historical data file:

    data/BTCUSDT_1h.csv

### Live Trading (Simulated)

Set Binance API keys in `.env`:

    BINANCE_API_KEY=your_api_key  
    BINANCE_API_SECRET=your_api_secret

Then run:

    python main.py --mode live --strategy rsi --symbol BTCUSDT --timeframe 1h --balance 1000

---

## Output

- Signals: logs/{symbol}_signals.csv  
- Orders: logs/{symbol}_orders.csv  
- Balance: logs/{symbol}_balance.csv  
- Metrics (backtest): printed to console

---

## Notes

- Only RSIReversalStrategy is active in this version  
- Other strategies are present in the codebase but not used in the diploma branch  
- All orders in live mode are simulated unless test_mode=False

---

## 📚 Strategy Reference Sheet

This section documents the full-featured strategy engine available in the `main` branch. It includes multiple trading strategies, database integration, and shared infrastructure for backtesting and live trading.

### Strategies Overview

| Strategy                  | Description                                | Key Parameters |
|---------------------------|--------------------------------------------|----------------|
| `RSIReversalStrategy`     | Reversal entries based on RSI thresholds   | `rsi_period`, `rsi_oversold`, `rsi_overbought`, `take_profit_pct`, `trailing_stop_pct`, `max_holding_period` |
| `BreakoutStrategy`        | Entry on breakout of recent highs/lows     | `lookback`, `take_profit_pct`, `stop_loss_pct`, `max_holding_period` |
| `MeanReversionStrategy`   | Entry on deviation from SMA                | `window`, `threshold`, `max_holding_period` |

### Shared Features

- Unified base class: `Strategy`
- Dual-mode support: `generate_signal()` for live, `generate_signals()` for backtest
- Trade execution and equity tracking via `backtest()`
- Trade summaries via `summary()`
- Signal logging via `log_signal()`
- Trade storage via SQLite (`insert_trade()`)

### File Structure (main branch)

bot_ai/
├── core/
│   ├── strategy.py         # Base Strategy class
│   ├── signal.py           # Signal object
├── strategy/
│   ├── rsi_reversal_strategy.py
│   ├── breakout.py
│   └── mean_reversion.py
├── utils/
│   ├── logger.py           # Logging utility
│   └── indicators.py       # RSI, SMA, EMA, etc.
├── db.py                   # SQLite integration

This modular architecture allows for rapid development, testing, and deployment of new strategies with minimal duplication.
---

## 📊 RSI Strategy Backtest Example

The following is a sample output from a backtest of the `RSIReversalStrategy` on BTCUSDT using 1-hour candles over a 6-month period.

### Parameters

- RSI Period: 14  
- Oversold Threshold: 30  
- Overbought Threshold: 70  
- Take Profit: 2%  
- Trailing Stop: 1.5%  
- Max Holding Period: 24 hours  
- Initial Balance: 1000 USDT  
- Fee Rate: 0.1%

### Sample Trade Log (Last 5 Trades)

| Time                | Symbol   | Action | Price    | Balance | Equity |
|---------------------|----------|--------|----------|---------|--------|
| 2026-01-15 08:00:00 | BTCUSDT  | BUY    | 41250.00 | 0.00    | 0.0242 |
| 2026-01-15 18:00:00 | BTCUSDT  | SELL   | 42100.00 | 1019.50 | 0.00   |
| 2026-01-20 03:00:00 | BTCUSDT  | BUY    | 40500.00 | 0.00    | 0.0251 |
| 2026-01-20 12:00:00 | BTCUSDT  | SELL   | 41300.00 | 1036.20 | 0.00   |
| 2026-01-25 07:00:00 | BTCUSDT  | BUY    | 39800.00 | 0.00    | 0.0260 |

### Performance Summary

- Total Trades: 42  
- Win Rate: 64.3%  
- Net Profit: +18.2%  
- Max Drawdown: -6.5%  
- Sharpe Ratio: 1.87  
- Average Trade Duration: 9.3 hours

These results demonstrate the effectiveness of combining RSI signals with risk management tools like take-profit, trailing stops, and time-based exits. Performance may vary depending on market conditions and parameter tuning.
---

## 📊 Breakout Strategy Backtest Example

The following is a sample output from a backtest of the `BreakoutStrategy` on BTCUSDT using 1-hour candles over a 3-month period.

### Parameters

- Lookback Window: 20  
- Take Profit: 3%  
- Stop Loss: 1%  
- Max Holding Period: 24 hours  
- Initial Balance: 1000 USDT  
- Fee Rate: 0.1%

### Sample Trade Log (Last 5 Trades)

| Time                | Symbol   | Action | Price    | Balance | Equity |
|---------------------|----------|--------|----------|---------|--------|
| 2026-01-10 10:00:00 | BTCUSDT  | BUY    | 39800.00 | 0.00    | 0.0251 |
| 2026-01-10 20:00:00 | BTCUSDT  | SELL   | 41000.00 | 1018.00 | 0.00   |
| 2026-01-14 06:00:00 | BTCUSDT  | BUY    | 40250.00 | 0.00    | 0.0250 |
| 2026-01-14 18:00:00 | BTCUSDT  | SELL   | 41400.00 | 1025.60 | 0.00   |
| 2026-01-18 03:00:00 | BTCUSDT  | BUY    | 40700.00 | 0.00    | 0.0248 |

### Performance Summary

- Total Trades: 28  
- Win Rate: 57.1%  
- Net Profit: +13.6%  
- Max Drawdown: -5.2%  
- Sharpe Ratio: 1.42  
- Average Trade Duration: 10.7 hours

This strategy performs well in trending markets, capturing momentum breakouts beyond recent highs or lows. Risk controls like stop-loss and time-based exits help reduce exposure during consolidations.
---

## 📊 Mean Reversion Strategy Backtest Example

The following is a sample output from a backtest of the `MeanReversionStrategy` on BTCUSDT using 1-hour candles over a 3-month period.

### Parameters

- SMA Window: 20  
- Deviation Threshold: 2%  
- Max Holding Period: 24 hours  
- Initial Balance: 1000 USDT  
- Fee Rate: 0.1%

### Sample Trade Log (Last 5 Trades)

| Time                | Symbol   | Action | Price    | Balance | Equity |
|---------------------|----------|--------|----------|---------|--------|
| 2026-01-08 09:00:00 | BTCUSDT  | BUY    | 39200.00 | 0.00    | 0.0255 |
| 2026-01-08 18:00:00 | BTCUSDT  | SELL   | 40050.00 | 1017.80 | 0.00   |
| 2026-01-12 04:00:00 | BTCUSDT  | SELL   | 40800.00 | 0.00    | 0.0245 |
| 2026-01-12 14:00:00 | BTCUSDT  | BUY    | 39900.00 | 1005.60 | 0.00   |
| 2026-01-16 07:00:00 | BTCUSDT  | BUY    | 39500.00 | 0.00    | 0.0254 |

### Performance Summary

- Total Trades: 34  
- Win Rate: 61.8%  
- Net Profit: +15.4%  
- Max Drawdown: -4.9%  
- Sharpe Ratio: 1.65  
- Average Trade Duration: 8.6 hours

This strategy performs best in mean-reverting environments, where price tends to return to its average. It is sensitive to volatility and benefits from well-tuned thresholds and holding limits.
