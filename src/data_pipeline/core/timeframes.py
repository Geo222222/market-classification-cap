"""Map CCXT-style timeframe strings to millisecond bar length."""

from __future__ import annotations


def timeframe_to_milliseconds(timeframe: str) -> int:
    """
    Convert strings like ``5s``, ``1m``, ``5m``, ``1h``, ``1d`` to bar length in ms.

    Raises ValueError if the timeframe is not supported.
    """
    tf = str(timeframe).strip().lower()
    if len(tf) < 2:
        raise ValueError(f"Invalid timeframe: {timeframe!r}")

    unit = tf[-1]
    try:
        n = int(tf[:-1])
    except ValueError as e:
        raise ValueError(f"Invalid timeframe: {timeframe!r}") from e
    if n <= 0:
        raise ValueError(f"Invalid timeframe: {timeframe!r}")

    mult = {
        "s": 1000,
        "m": 60_000,
        "h": 3_600_000,
        "d": 86_400_000,
    }.get(unit)
    if mult is None:
        raise ValueError(f"Unsupported timeframe unit in: {timeframe!r}")
    return n * mult


def bar_open_timestamp_ms(trade_ts_ms: int, period_ms: int) -> int:
    """UTC-aligned bar open (same convention as typical exchange candles)."""
    return (int(trade_ts_ms) // period_ms) * period_ms
