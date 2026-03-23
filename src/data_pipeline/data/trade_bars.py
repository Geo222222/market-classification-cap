"""
Aggregate tick trades into OHLCV bars aligned to configured timeframes.

Bars are only written after the interval is **closed** in wall-clock UTC
(``bar_open + period <= now``), matching the idea of completed candles.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..core.timeframes import bar_open_timestamp_ms


@dataclass
class _BarScratch:
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0
    trade_count: int = 0
    open_ts: int = 0  # ms of trade that set open
    close_ts: int = 0  # ms of trade that set close


@dataclass
class TradeOhlcvAccumulator:
    """Per (symbol, timeframe) rolling state for trade-derived candles."""

    period_ms: int
    bars: dict[int, _BarScratch] = field(default_factory=dict)

    def ingest_sorted_trades(self, trade_rows: list[dict]) -> None:
        """Merge trades (each dict needs timestamp_ms, price, amount); rows should be time-sorted."""
        p = self.period_ms
        for t in trade_rows:
            try:
                ts = int(float(t.get("timestamp_ms", 0) or 0))
                price = float(t.get("price", 0.0) or 0.0)
                amt = float(t.get("amount", 0.0) or 0.0)
            except (TypeError, ValueError):
                continue
            if ts <= 0 or price <= 0:
                continue

            b0 = bar_open_timestamp_ms(ts, p)
            bar = self.bars.get(b0)
            if bar is None:
                self.bars[b0] = _BarScratch(
                    open=price,
                    high=price,
                    low=price,
                    close=price,
                    volume=amt,
                    trade_count=1,
                    open_ts=ts,
                    close_ts=ts,
                )
                continue

            bar.high = max(bar.high, price)
            bar.low = min(bar.low, price)
            bar.volume += amt
            bar.trade_count += 1
            if ts >= bar.close_ts:
                bar.close_ts = ts
                bar.close = price
            if ts <= bar.open_ts:
                bar.open_ts = ts
                bar.open = price

    def pop_closed_bars(self, wall_time_ms: int, last_flushed_open: int) -> list[dict]:
        """
        Return CSV-ready rows for bars that are fully closed and not yet flushed.

        ``last_flushed_open`` is the bar_open ``timestamp_ms`` of the last row on disk.
        Use ``-1`` when the CSV is empty so bucket ``0`` is not mistaken for already flushed.
        """
        now = int(wall_time_ms)
        p = self.period_ms
        out: list[dict] = []
        to_del: list[int] = []

        for b0, bar in sorted(self.bars.items()):
            if b0 + p > now:
                continue  # still forming
            if last_flushed_open >= 0 and b0 <= last_flushed_open:
                to_del.append(b0)
                continue
            out.append(
                {
                    "timestamp_ms": b0,
                    "open": bar.open,
                    "high": bar.high,
                    "low": bar.low,
                    "close": bar.close,
                    "volume": bar.volume,
                    "trade_count": bar.trade_count,
                }
            )
            to_del.append(b0)

        for b0 in to_del:
            self.bars.pop(b0, None)

        return out


def trade_ohlcv_csv_fieldnames() -> list[str]:
    return [
        "timestamp_ms",
        "symbol",
        "timeframe",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "trade_count",
        "source",
    ]
