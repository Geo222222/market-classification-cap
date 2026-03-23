# `data_pipeline` (in-repo, incremental)

## Package layout

- **`core/`** — `paths`, `config` (`AppConfig`, `load_config`), `context`, `errors`, `utils`, `cleaning`, `timeframes`
- **`data/storage.py`** — CSV append / last-column helpers
- **`data/trade_bars.py`** — aggregate tick trades into OHLCV for each configured timeframe
- **`services/`** — `exchange` (`create_exchange`), `market` (OHLCV, trades, tickers, order book), `orders` (open orders)
- **`app/`** — `LiveDataCollector`, reconciliation backfill (`reconcile.py`)
- **`ui/`** — Tkinter + matplotlib live CSV chart
- **`main.py`** — loads config and opens `CollectorApp`
- **`app_config.yaml`** — default app settings (tracked)

Collector CSV files under `data/**` are **gitignored**; only `data/.gitkeep` is tracked.

### OHLCV: exchange vs trade-aggregated

| File pattern | Source |
|--------------|--------|
| `data/ohlcv/ohlcv_{SYMBOL}_{tf}.csv` | Pre-aggregated candles from the exchange API (`fetch_ohlcv`). |
| `data/ohlcv/ohlcv_trades_{SYMBOL}_{tf}.csv` | Bars **built from your stored ticks** in `data/trades/`. Intervals = **`trade_aggregate_timeframes`** (default: `5s`–`45s` if omitted or empty; independent of exchange `timeframes`). |

Trade bars are appended only after the interval is **closed** in wall-clock UTC (same alignment as typical exchange candle opens). Extra columns: `trade_count`, `source=trades`.

## Reference copy (local only)

**`progress/data_pipeline/`** (repo root, **gitignored**) holds the full previous tree.

## Run

```bash
pip install -e .
python -m data_pipeline
# or: python run_collector.py
```

This opens the **Project Live Collector** window (Start / Pause / Resume / Stop / Reconcile).

Requires **`credentials.yaml`** at the repo root (gitignored) for **Start** (exchange login via CCXT).
