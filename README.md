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
## 📘 Strategy Modules Overview

This section documents the core trading strategies implemented in the `bot_ai/strategy/` directory. Each strategy inherits from the base `Strategy` class and supports both backtesting and live trading modes with integrated logging and database storage.

### Strategies

| Strategy              | Description                                      | Key Parameters                          |
|-----------------------|--------------------------------------------------|------------------------------------------|
| `RSIReversalStrategy` | Reversal strategy based on RSI oversold/overbought levels | `rsi_period`, `rsi_oversold`, `rsi_overbought`, `take_profit_pct`, `trailing_stop_pct`, `max_holding_period` |
| `BreakoutStrategy`    | Breakout strategy using rolling high/low levels  | `lookback`, `take_profit_pct`, `stop_loss_pct`, `max_holding_period` |
| `MeanReversionStrategy` | Mean reversion strategy based on SMA deviation | `window`, `threshold`, `max_holding_period` |

### Shared Features

- All strategies support:
  - `generate_signal(df)` for live mode
  - `generate_signals(df)` for backtesting
  - `backtest(df)` with fee and equity tracking
  - `summary(symbol)` to return trade history
- Signals are logged via `log_signal()`
- Trades are stored in SQLite via `insert_trade()`

### File Structure

bot_ai/
├── core/
│   ├── signal.py         # Signal class
│   └── strategy.py       # Base Strategy class
├── strategy/
│   ├── rsi_reversal_strategy.py
│   ├── breakout.py
│   └── mean_reversion.py
├── utils/
│   └── logger.py         # log_signal()
└── db.py                 # SQLite integration
