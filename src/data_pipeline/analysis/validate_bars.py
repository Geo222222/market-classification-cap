"""
validate_bars.py

Generates two research diagnostics from existing CSV candle artifacts:

1) Bar coverage
   For each (symbol, timeframe, source) candle series, compute expected vs
   observed buckets and report missing bucket counts + coverage %.

2) Alignment validation
   For overlapping series, compare OHLCV values from trade-built bars
   (ohlcv_trades_*) vs exchange bars (ohlcv_*), producing summary deltas.

This is intended to run after a collection session and produce local report
CSVs under:
  <config.output_dir>/validation/

Reports are written as CSV to remain consistent with existing `.gitignore`
patterns for local data outputs.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from ..core.config import load_config
from ..core.timeframes import timeframe_to_milliseconds


SOURCE_EXCHANGE = "exchange"
SOURCE_TRADES = "trades"


def _safe_float(v: Any) -> float | None:
    if v is None:
        return None
    s = str(v).strip()
    if not s:
        return None
    try:
        return float(s)
    except Exception:
        return None


def _parse_int_ms(v: Any) -> int | None:
    f = _safe_float(v)
    if f is None:
        return None
    try:
        return int(float(f))
    except Exception:
        return None


def _parse_candle_filename(path: Path) -> tuple[str, str, str]:
    """
    Return (source, symbol_safe, timeframe) from files like:
      - ohlcv_BTC_USDT_USDT_1m.csv
      - ohlcv_trades_BTC_USDT_USDT_5s.csv
    """
    stem = path.stem  # without .csv
    parts = stem.split("_")
    if stem.startswith("ohlcv_trades_"):
        # ohlcv_trades_<SYM>_<TF>
        timeframe = parts[-1]
        symbol_safe = "_".join(parts[2:-1])
        return SOURCE_TRADES, symbol_safe, timeframe
    if stem.startswith("ohlcv_"):
        # ohlcv_<SYM>_<TF>
        timeframe = parts[-1]
        symbol_safe = "_".join(parts[1:-1])
        return SOURCE_EXCHANGE, symbol_safe, timeframe
    raise ValueError(f"Unrecognized candle filename: {path}")


def _read_candles(path: Path) -> list[dict[str, Any]]:
    """
    Read a CSV candle file into a list of rows.
    Expected columns include at least:
      - timestamp_ms
      - open, high, low, close, volume
    """
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8", errors="replace", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # keep raw row for later typed access
            rows.append(row)
    return rows


def _extract_ohlcvs(rows: Iterable[dict[str, Any]]) -> dict[int, dict[str, float]]:
    """
    Map timestamp_ms -> OHLCV dict.
    If duplicates exist for the same timestamp, later rows win.
    """
    out: dict[int, dict[str, float]] = {}
    for r in rows:
        ts = _parse_int_ms(r.get("timestamp_ms"))
        if ts is None:
            continue
        o = _safe_float(r.get("open"))
        h = _safe_float(r.get("high"))
        l = _safe_float(r.get("low"))
        c = _safe_float(r.get("close"))
        v = _safe_float(r.get("volume"))
        if o is None or h is None or l is None or c is None or v is None:
            continue
        out[ts] = {"open": o, "high": h, "low": l, "close": c, "volume": v}
    return out


@dataclass
class CoverageSummary:
    symbol_safe: str
    timeframe: str
    source: str
    start_ms: int
    end_ms: int
    expected_bars: int
    observed_bars: int
    missing_bars: int
    coverage_pct: float
    max_gap_bars: int


def _coverage_for_series(
    rows: list[dict[str, Any]],
    symbol_safe: str,
    timeframe: str,
    source: str,
) -> CoverageSummary | None:
    period_ms = timeframe_to_milliseconds(timeframe)

    ts_list: list[int] = []
    for r in rows:
        ts = _parse_int_ms(r.get("timestamp_ms"))
        if ts is None:
            continue
        ts_list.append(ts)
    if not ts_list:
        return None

    ts_set = sorted(set(ts_list))
    start_ms = ts_set[0]
    end_ms = ts_set[-1]

    expected_bars = ((end_ms - start_ms) // period_ms) + 1
    observed_bars = len(ts_set)
    missing_bars = max(0, expected_bars - observed_bars)
    coverage_pct = (observed_bars / expected_bars) * 100.0 if expected_bars > 0 else 0.0

    # max consecutive missing bucket run (in bars)
    max_gap_bars = 0
    for prev, curr in zip(ts_set[:-1], ts_set[1:]):
        # if gaps are misaligned, this indicates irregular timestamps
        gap_bars = (curr - prev) // period_ms - 1
        if gap_bars > max_gap_bars:
            max_gap_bars = gap_bars

    return CoverageSummary(
        symbol_safe=symbol_safe,
        timeframe=timeframe,
        source=source,
        start_ms=start_ms,
        end_ms=end_ms,
        expected_bars=expected_bars,
        observed_bars=observed_bars,
        missing_bars=missing_bars,
        coverage_pct=coverage_pct,
        max_gap_bars=max_gap_bars,
    )


def _align_validation(
    exchange_rows: list[dict[str, Any]],
    trades_rows: list[dict[str, Any]],
    symbol_safe: str,
    timeframe: str,
    period_ms: int,
    price_abs_tol: float,
    price_rel_tol: float,
    vol_abs_tol: float,
    vol_rel_tol: float,
) -> dict[str, Any]:
    ex = _extract_ohlcvs(exchange_rows)
    tr = _extract_ohlcvs(trades_rows)

    overlap_ts = sorted(set(ex.keys()) & set(tr.keys()))
    if not overlap_ts:
        return {
            "symbol_safe": symbol_safe,
            "timeframe": timeframe,
            "overlap_expected_bars": 0,
            "matched_bars": 0,
            "match_rate_pct": 0.0,
            "mean_abs_open_diff": "",
            "p95_abs_open_diff": "",
            "mean_abs_volume_diff": "",
            "max_abs_close_diff": "",
            "open_within_tol_pct": "",
            "volume_within_tol_pct": "",
        }

    overlap_start = max(min(ex.keys()), min(tr.keys()))
    overlap_end = min(max(ex.keys()), max(tr.keys()))
    overlap_expected_bars = ((overlap_end - overlap_start) // period_ms) + 1 if overlap_end >= overlap_start else 0

    def within(a: float, b: float, abs_tol: float, rel_tol: float) -> bool:
        d = abs(a - b)
        if d <= abs_tol:
            return True
        denom = max(abs(b), 1e-12)
        return (d / denom) <= rel_tol

    diffs_open: list[float] = []
    diffs_vol: list[float] = []
    max_close_diff = 0.0
    open_within = 0
    vol_within = 0

    for ts in overlap_ts:
        eo = ex[ts]
        to = tr[ts]
        open_d = abs(eo["open"] - to["open"])
        vol_d = abs(eo["volume"] - to["volume"])
        close_d = abs(eo["close"] - to["close"])
        diffs_open.append(open_d)
        diffs_vol.append(vol_d)
        if close_d > max_close_diff:
            max_close_diff = close_d

        if within(eo["open"], to["open"], price_abs_tol, price_rel_tol):
            open_within += 1
        if within(eo["volume"], to["volume"], vol_abs_tol, vol_rel_tol):
            vol_within += 1

    diffs_open_sorted = sorted(diffs_open)
    diffs_vol_sorted = sorted(diffs_vol)
    p95_open = diffs_open_sorted[int(0.95 * (len(diffs_open_sorted) - 1))] if diffs_open_sorted else 0.0
    mean_open = sum(diffs_open) / len(diffs_open) if diffs_open else 0.0
    mean_vol = sum(diffs_vol) / len(diffs_vol) if diffs_vol else 0.0

    match_rate_pct = (len(overlap_ts) / overlap_expected_bars) * 100.0 if overlap_expected_bars > 0 else 0.0

    return {
        "symbol_safe": symbol_safe,
        "timeframe": timeframe,
        "overlap_expected_bars": overlap_expected_bars,
        "matched_bars": len(overlap_ts),
        "match_rate_pct": match_rate_pct,
        "mean_abs_open_diff": mean_open,
        "p95_abs_open_diff": p95_open,
        "mean_abs_volume_diff": mean_vol,
        "max_abs_close_diff": max_close_diff,
        "open_within_tol_pct": (open_within / len(overlap_ts)) * 100.0 if overlap_ts else 0.0,
        "volume_within_tol_pct": (vol_within / len(overlap_ts)) * 100.0 if overlap_ts else 0.0,
    }


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate candle coverage + trade-vs-exchange alignment.")
    parser.add_argument("--symbol", default=None, help="Filter by symbol_safe (e.g. BTC_USDT_USDT).")
    parser.add_argument("--timeframe", default=None, help="Filter by timeframe (e.g. 5s, 10s, 1m).")
    parser.add_argument("--output-dir", default=None, help="Override output dir (defaults to config.output_dir).")
    parser.add_argument("--price-abs-tol", type=float, default=1e-6)
    parser.add_argument("--price-rel-tol", type=float, default=1e-3)
    parser.add_argument("--vol-abs-tol", type=float, default=1e-9)
    parser.add_argument("--vol-rel-tol", type=float, default=5e-2)
    args = parser.parse_args()

    cfg = load_config(None)
    base_out = Path(args.output_dir) if args.output_dir else Path(cfg.output_dir)
    ohlcv_dir = base_out / "ohlcv"
    validation_dir = base_out / "validation"
    run_ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    if not ohlcv_dir.exists():
        raise FileNotFoundError(f"Expected candle directory not found: {ohlcv_dir}")

    # Collect file paths
    ex_map: dict[tuple[str, str], Path] = {}
    tr_map: dict[tuple[str, str], Path] = {}

    for p in ohlcv_dir.glob("ohlcv_*.csv"):
        try:
            src, sym_safe, tf = _parse_candle_filename(p)
        except ValueError:
            continue
        if args.symbol and sym_safe != args.symbol:
            continue
        if args.timeframe and tf != args.timeframe:
            continue
        if src == SOURCE_EXCHANGE:
            ex_map[(sym_safe, tf)] = p

    for p in ohlcv_dir.glob("ohlcv_trades_*.csv"):
        try:
            src, sym_safe, tf = _parse_candle_filename(p)
        except ValueError:
            continue
        if args.symbol and sym_safe != args.symbol:
            continue
        if args.timeframe and tf != args.timeframe:
            continue
        if src == SOURCE_TRADES:
            tr_map[(sym_safe, tf)] = p

    # 1) Coverage reports (both sources)
    coverage_rows: list[dict[str, Any]] = []
    coverage_by_key: dict[tuple[str, str, str], CoverageSummary] = {}

    for (sym_safe, tf), p in ex_map.items():
        rows = _read_candles(p)
        cov = _coverage_for_series(rows, symbol_safe=sym_safe, timeframe=tf, source=SOURCE_EXCHANGE)
        if cov is None:
            continue
        coverage_by_key[(sym_safe, tf, SOURCE_EXCHANGE)] = cov

    for (sym_safe, tf), p in tr_map.items():
        rows = _read_candles(p)
        cov = _coverage_for_series(rows, symbol_safe=sym_safe, timeframe=tf, source=SOURCE_TRADES)
        if cov is None:
            continue
        coverage_by_key[(sym_safe, tf, SOURCE_TRADES)] = cov

    for (sym_safe, tf, src), cov in sorted(coverage_by_key.items()):
        coverage_rows.append(
            {
                "symbol_safe": sym_safe,
                "timeframe": tf,
                "source": src,
                "start_ms": cov.start_ms,
                "end_ms": cov.end_ms,
                "expected_bars": cov.expected_bars,
                "observed_bars": cov.observed_bars,
                "missing_bars": cov.missing_bars,
                "coverage_pct": cov.coverage_pct,
                "max_gap_bars": cov.max_gap_bars,
            }
        )

    coverage_fieldnames = [
        "symbol_safe",
        "timeframe",
        "source",
        "start_ms",
        "end_ms",
        "expected_bars",
        "observed_bars",
        "missing_bars",
        "coverage_pct",
        "max_gap_bars",
    ]

    coverage_out = validation_dir / f"bar_coverage_report_{run_ts}.csv"
    _write_csv(coverage_out, coverage_fieldnames, coverage_rows)

    # 2) Alignment validation between sources (only matching keys)
    overlap_keys = sorted(set(ex_map.keys()) & set(tr_map.keys()))
    alignment_rows: list[dict[str, Any]] = []

    for sym_safe, tf in overlap_keys:
        ex_rows = _read_candles(ex_map[(sym_safe, tf)])
        tr_rows = _read_candles(tr_map[(sym_safe, tf)])
        period_ms = timeframe_to_milliseconds(tf)
        result = _align_validation(
            exchange_rows=ex_rows,
            trades_rows=tr_rows,
            symbol_safe=sym_safe,
            timeframe=tf,
            period_ms=period_ms,
            price_abs_tol=args.price_abs_tol,
            price_rel_tol=args.price_rel_tol,
            vol_abs_tol=args.vol_abs_tol,
            vol_rel_tol=args.vol_rel_tol,
        )
        alignment_rows.append(result)

    alignment_fieldnames = [
        "symbol_safe",
        "timeframe",
        "overlap_expected_bars",
        "matched_bars",
        "match_rate_pct",
        "mean_abs_open_diff",
        "p95_abs_open_diff",
        "mean_abs_volume_diff",
        "max_abs_close_diff",
        "open_within_tol_pct",
        "volume_within_tol_pct",
    ]
    alignment_out = validation_dir / f"bar_alignment_report_{run_ts}.csv"
    _write_csv(alignment_out, alignment_fieldnames, alignment_rows)

    # Human-readable summary
    print(f"[validate_bars] coverage_report: {coverage_out}")
    print(f"[validate_bars] alignment_report: {alignment_out}")
    if coverage_rows:
        best = sorted(coverage_rows, key=lambda r: r["coverage_pct"], reverse=True)[:5]
        print("[validate_bars] top coverage entries:")
        for r in best:
            print(f"  {r['source']} {r['symbol_safe']} {r['timeframe']} -> {r['coverage_pct']:.2f}%")
    if alignment_rows:
        print("[validate_bars] alignment entries:")
        for r in alignment_rows[:10]:
            print(
                f"  {r['symbol_safe']} {r['timeframe']}: matched={r['matched_bars']} "
                f"match_rate={r['match_rate_pct']:.1f}% open_within_tol={r['open_within_tol_pct']}%"
            )


if __name__ == "__main__":
    main()

