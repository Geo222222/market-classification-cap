"""Backfill/reconciliation routines for missed data windows."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from ..data.storage import append_rows_csv, last_numeric_value
from ..services.market import fetch_ohlcv, fetch_trades


def _safe_symbol(symbol: str) -> str:
    return symbol.replace("/", "_").replace(":", "_")


def _ohlcv_csv_path(base_dir: str | Path, symbol: str, timeframe: str) -> Path:
    return Path(base_dir) / "ohlcv" / f"ohlcv_{_safe_symbol(symbol)}_{timeframe}.csv"


def _trades_csv_path(base_dir: str | Path, symbol: str) -> Path:
    return Path(base_dir) / "trades" / f"trades_{_safe_symbol(symbol)}.csv"


def reconcile_ohlcv_symbol_timeframe(base_dir: str | Path, symbol: str, timeframe: str, chunk_limit: int = 1000, log_cb=None) -> int:
    """Backfill OHLCV rows after the last stored timestamp (ms)."""
    path = _ohlcv_csv_path(base_dir, symbol, timeframe)
    last_ts = last_numeric_value(path, "timestamp_ms")
    since_ms = (last_ts + 1) if last_ts is not None else None
    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

    inserted = 0
    loops = 0
    while True:
        loops += 1
        if loops > 500:
            break

        df = fetch_ohlcv(symbol, timeframe, limit=chunk_limit, since=since_ms)
        if df is None or df.empty:
            break

        rows = []
        max_seen = since_ms or 0
        for _, row in df.iterrows():
            ts_raw = row.get("timestamp")
            try:
                ts_ms = int(ts_raw.value // 10**6) if hasattr(ts_raw, "value") else int(float(ts_raw))
            except Exception:
                continue

            if last_ts is not None and ts_ms <= last_ts:
                continue
            if ts_ms > now_ms:
                continue

            rows.append(
                {
                    "timestamp_ms": ts_ms,
                    "symbol": symbol,
                    "timeframe": timeframe,
                    "open": float(row.get("open", 0.0)),
                    "high": float(row.get("high", 0.0)),
                    "low": float(row.get("low", 0.0)),
                    "close": float(row.get("close", 0.0)),
                    "volume": float(row.get("volume", 0.0)),
                }
            )
            if ts_ms > max_seen:
                max_seen = ts_ms

        if not rows:
            break

        inserted += append_rows_csv(
            path,
            ["timestamp_ms", "symbol", "timeframe", "open", "high", "low", "close", "volume"],
            rows,
        )

        if max_seen <= (since_ms or 0):
            break

        since_ms = max_seen + 1
        if max_seen >= now_ms:
            break

    if log_cb:
        log_cb(f"Reconcile OHLCV {symbol} {timeframe}: +{inserted} rows")
    return inserted


def reconcile_trades_symbol(base_dir: str | Path, symbol: str, chunk_limit: int = 1000, log_cb=None) -> int:
    """Backfill trade rows after the last stored trade timestamp (ms)."""
    path = _trades_csv_path(base_dir, symbol)
    last_ts = last_numeric_value(path, "timestamp_ms")
    since_ms = (last_ts + 1) if last_ts is not None else None

    inserted = 0
    loops = 0
    while True:
        loops += 1
        if loops > 1000:
            break

        trades = fetch_trades(symbol, since=since_ms, limit=chunk_limit)
        if not trades:
            break

        rows = []
        max_seen = since_ms or 0
        for t in trades:
            try:
                ts_ms = int(float(t.get("timestamp", 0) or 0))
            except Exception:
                continue
            if ts_ms <= 0:
                continue
            if last_ts is not None and ts_ms <= last_ts:
                continue

            rows.append(
                {
                    "timestamp_ms": ts_ms,
                    "symbol": str(t.get("symbol", symbol) or symbol),
                    "trade_id": str(t.get("id", "") or ""),
                    "side": str(t.get("side", "") or ""),
                    "price": float(t.get("price", 0.0) or 0.0),
                    "amount": float(t.get("amount", 0.0) or 0.0),
                    "cost": float(t.get("cost", 0.0) or 0.0),
                    "datetime": str(t.get("datetime", "") or ""),
                }
            )
            if ts_ms > max_seen:
                max_seen = ts_ms

        if not rows:
            break

        inserted += append_rows_csv(
            path,
            ["timestamp_ms", "symbol", "trade_id", "side", "price", "amount", "cost", "datetime"],
            rows,
        )

        if max_seen <= (since_ms or 0):
            break
        since_ms = max_seen + 1

    if log_cb:
        log_cb(f"Reconcile trades {symbol}: +{inserted} rows")
    return inserted
