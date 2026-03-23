"""Entry point for ``python -m data_pipeline`` and ``run_collector.py``."""

from __future__ import annotations

from .core.config import load_config


def run(config_path: str | None = None) -> None:
    """
    Smoke entry: load YAML config and print summary.

    Full UI lives in ``progress/data_pipeline/`` until ``ui`` + ``app`` are restored.
    """
    cfg = load_config(config_path)
    print()
    print("  data_pipeline: core loaded")
    print(f"    exchange: {cfg.exchange_name!r}")
    print(f"    symbols:  {len(cfg.symbols)}  timeframes: {cfg.timeframes}")
    print(f"    output:   {cfg.output_dir}")
    print("  (Next: services + app + ui for live collector.)")
    print()


if __name__ == "__main__":
    run()
