"""Configuration loader for the standalone project collector app."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .paths import resolve_config_path, resolve_under_package


@dataclass
class AppConfig:
    exchange_name: str = "htx"
    account_name: str = ""
    symbols: list[str] = field(default_factory=lambda: ["ETH/USDT:USDT", "BTC/USDT:USDT"])
    timeframes: list[str] = field(default_factory=lambda: ["1m", "5m"])
    # Relative paths are resolved against the data_pipeline package root (see load_config).
    output_dir: str = "data"

    # polling cadences (seconds)
    interval_orders_s: float = 8.0
    interval_orderbook_s: float = 3.0
    interval_tickers_s: float = 10.0
    interval_trades_s: float = 5.0
    interval_ohlcv_s: float = 20.0

    # fetch limits
    trades_limit: int = 200
    ohlcv_limit: int = 300
    reconcile_chunk_limit: int = 1000


_DEFAULT = AppConfig()


def default_config_dict() -> dict[str, Any]:
    return {
        "app": {
            "exchange_name": _DEFAULT.exchange_name,
            "account_name": _DEFAULT.account_name,
            "symbols": _DEFAULT.symbols,
            "timeframes": _DEFAULT.timeframes,
            "output_dir": _DEFAULT.output_dir,
            "interval_orders_s": _DEFAULT.interval_orders_s,
            "interval_orderbook_s": _DEFAULT.interval_orderbook_s,
            "interval_tickers_s": _DEFAULT.interval_tickers_s,
            "interval_trades_s": _DEFAULT.interval_trades_s,
            "interval_ohlcv_s": _DEFAULT.interval_ohlcv_s,
            "trades_limit": _DEFAULT.trades_limit,
            "ohlcv_limit": _DEFAULT.ohlcv_limit,
            "reconcile_chunk_limit": _DEFAULT.reconcile_chunk_limit,
        }
    }


def ensure_config_file(path: Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(default_config_dict(), f, sort_keys=False)
    return path


def load_config(path: str | Path | None = None) -> AppConfig:
    """Load config from YAML. Paths in ``output_dir`` are resolved to absolute (package-relative if not absolute)."""
    p = resolve_config_path(path)
    p = ensure_config_file(p)
    with p.open("r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}

    app = raw.get("app", {}) if isinstance(raw, dict) else {}

    def _flt(name: str, default: float) -> float:
        try:
            return float(app.get(name, default))
        except Exception:
            return default

    def _int(name: str, default: int) -> int:
        try:
            return int(app.get(name, default))
        except Exception:
            return default

    symbols = app.get("symbols", _DEFAULT.symbols)
    timeframes = app.get("timeframes", _DEFAULT.timeframes)

    raw_output = str(app.get("output_dir", _DEFAULT.output_dir) or _DEFAULT.output_dir)

    cfg = AppConfig(
        exchange_name=str(app.get("exchange_name", _DEFAULT.exchange_name) or _DEFAULT.exchange_name),
        account_name=str(app.get("account_name", _DEFAULT.account_name) or ""),
        symbols=[str(s).strip() for s in symbols if str(s).strip()] if isinstance(symbols, list) else list(_DEFAULT.symbols),
        timeframes=[str(tf).strip() for tf in timeframes if str(tf).strip()] if isinstance(timeframes, list) else list(_DEFAULT.timeframes),
        output_dir=raw_output,
        interval_orders_s=max(1.0, _flt("interval_orders_s", _DEFAULT.interval_orders_s)),
        interval_orderbook_s=max(1.0, _flt("interval_orderbook_s", _DEFAULT.interval_orderbook_s)),
        interval_tickers_s=max(1.0, _flt("interval_tickers_s", _DEFAULT.interval_tickers_s)),
        interval_trades_s=max(1.0, _flt("interval_trades_s", _DEFAULT.interval_trades_s)),
        interval_ohlcv_s=max(1.0, _flt("interval_ohlcv_s", _DEFAULT.interval_ohlcv_s)),
        trades_limit=max(1, _int("trades_limit", _DEFAULT.trades_limit)),
        ohlcv_limit=max(10, _int("ohlcv_limit", _DEFAULT.ohlcv_limit)),
        reconcile_chunk_limit=max(100, _int("reconcile_chunk_limit", _DEFAULT.reconcile_chunk_limit)),
    )
    if not cfg.symbols:
        cfg.symbols = list(_DEFAULT.symbols)
    if not cfg.timeframes:
        cfg.timeframes = list(_DEFAULT.timeframes)

    cfg.output_dir = str(resolve_under_package(cfg.output_dir))
    return cfg
