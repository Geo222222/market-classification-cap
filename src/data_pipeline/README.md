# `data_pipeline` (in-repo, incremental)

## In this commit: `core` + `data.storage`

- **`core/`** — `paths`, `config` (`AppConfig`, `load_config`), `context`, `errors`, `utils`, `cleaning`
- **`data/storage.py`** — CSV append / last-column helpers
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

This loads config and prints a summary. The Tk UI returns when `services/`, `app/`, and `ui/` are added back.
