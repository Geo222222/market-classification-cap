"""Data cleanup and normalization for live exchange payloads."""

from __future__ import annotations

from typing import Any

try:
    import pandas as pd
except Exception:  # pragma: no cover - runtime env dependent
    pd = None


# -------- Orders --------
def clean_orders(orders: Any) -> list[dict]:
    """Normalize open-order list payload."""
    if not isinstance(orders, list):
        return []
    return [o for o in orders if isinstance(o, dict)]


# -------- OHLCV --------
def clean_ohlcv_df(df):
    """Normalize OHLCV dataframe for plotting/analysis safety."""
    if pd is None:
        return df
    if df is None or df.empty:
        return None

    required_cols = ["timestamp", "open", "high", "low", "close", "volume"]
    for col in required_cols:
        if col not in df.columns:
            return None

    fixed = df.copy()

    # Force numeric columns where possible.
    for col in ["open", "high", "low", "close", "volume"]:
        fixed[col] = pd.to_numeric(fixed[col], errors="coerce")

    # Forward-fill then drop still-invalid rows.
    fixed = fixed.ffill()
    fixed = fixed.dropna(subset=["open", "high", "low", "close", "volume"])
    if fixed.empty:
        return None

    # Ensure high >= low.
    invalid_rows = fixed["high"] < fixed["low"]
    if invalid_rows.any():
        temp = fixed.loc[invalid_rows, "high"].copy()
        fixed.loc[invalid_rows, "high"] = fixed.loc[invalid_rows, "low"]
        fixed.loc[invalid_rows, "low"] = temp

    return fixed


# -------- Trades --------
def clean_trades(trades: Any) -> list[dict]:
    """Normalize trades list payload."""
    if not isinstance(trades, list):
        return []
    return [t for t in trades if isinstance(t, dict)]


# -------- Tickers --------
def clean_ticker(ticker: Any) -> dict | None:
    """Normalize a ticker payload."""
    if not isinstance(ticker, dict):
        return None
    return ticker


def clean_tickers(tickers: Any) -> dict:
    """Normalize tickers dictionary payload."""
    if not isinstance(tickers, dict):
        return {}
    return {k: v for k, v in tickers.items() if isinstance(v, dict)}


# -------- Order Book --------
def clean_order_book(order_book: Any) -> dict | None:
    """Normalize an orderbook payload."""
    if not isinstance(order_book, dict):
        return None

    bids = order_book.get("bids")
    asks = order_book.get("asks")
    if not isinstance(bids, list) or not isinstance(asks, list):
        return None

    # Keep only [price, size] pairs.
    norm_bids = [row for row in bids if isinstance(row, (list, tuple)) and len(row) >= 2]
    norm_asks = [row for row in asks if isinstance(row, (list, tuple)) and len(row) >= 2]

    cleaned = dict(order_book)
    cleaned["bids"] = norm_bids
    cleaned["asks"] = norm_asks
    return cleaned
