"""Entry point for ``python -m data_pipeline`` and ``run_collector.py``."""

from __future__ import annotations

from .core.config import load_config
from .ui.app import CollectorApp


def run(config_path: str | None = None) -> None:
    cfg = load_config(config_path)
    app = CollectorApp(cfg)
    app.mainloop()


if __name__ == "__main__":
    run()
