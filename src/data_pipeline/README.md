# `data_pipeline` (in-repo, incremental)

## Package layout

- **`core/`** — `paths`, `config` (`AppConfig`, `load_config`), `context`, `errors`, `utils`, `cleaning`
- **`data/storage.py`** — CSV append / last-column helpers
- **`services/`** — `exchange` (`create_exchange`), `market` (OHLCV, trades, tickers, order book), `orders` (open orders)
- **`app_config.yaml`** — default app settings (tracked)

Collector CSV files under `data/**` are **gitignored**; only `data/.gitkeep` is tracked.

## Reference copy (local only)

**`progress/data_pipeline/`** (repo root, **gitignored**) holds the full previous tree.

## Run

```bash
pip install -e .
python -m data_pipeline
# or: python run_collector.py
```

This loads config and prints a summary. The Tk UI returns when `app/` and `ui/` are wired back in.

Requires **`credentials.yaml`** at the repo root (gitignored) for live API calls via `services.exchange.create_exchange`.
