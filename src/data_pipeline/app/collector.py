"""Background live data collector with pause/stop and reconciliation support."""

from __future__ import annotations

import json
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from ..core.config import AppConfig
from ..core.context import set_exchange
from ..core.timeframes import bar_open_timestamp_ms, timeframe_to_milliseconds
from ..data.storage import append_rows_csv, ensure_dir, last_numeric_value
from ..data.trade_bars import TradeOhlcvAccumulator, trade_ohlcv_csv_fieldnames
from ..services.exchange import create_exchange
from ..services.market import fetch_ohlcv, fetch_order_book, fetch_tickers, fetch_trades
from ..services.orders import fetch_open_orders
from .reconcile import reconcile_ohlcv_symbol_timeframe, reconcile_trades_symbol

LogCB = Callable[[str], None]
StateCB = Callable[[str], None]


class LiveDataCollector:
    def __init__(self, config: AppConfig, log_cb: LogCB | None = None, state_cb: StateCB | None = None):
        self.config = config
        self.log_cb = log_cb or (lambda _msg: None)
        self.state_cb = state_cb or (lambda _state: None)

        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._running = False

        self._last_polled = {
            "orders": 0.0,
            "orderbook": 0.0,
            "tickers": 0.0,
            "trades": 0.0,
            "ohlcv": 0.0,
        }

        self._last_trade_ts: dict[str, int] = {}
        self._last_ohlcv_ts: dict[tuple[str, str], int] = {}
        # (symbol, timeframe) -> accumulator for OHLCV built from ticks (same TF as exchange config)
        self._trade_ohlcv_accum: dict[tuple[str, str], TradeOhlcvAccumulator] = {}

        self.account_name = ""
        self.exchange_name = ""

    @property
    def running(self) -> bool:
        return self._running

    def _log(self, msg: str) -> None:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
        self.log_cb(f"[{ts}] {msg}")

    def start(self) -> None:
        if self._running:
            self._log("Collector already running")
            return

        self._stop_event.clear()
        self._pause_event.clear()

        self.account_name, self.exchange_name, exchange = create_exchange(
            account_name=self.config.account_name,
            exchange_name_override=self.config.exchange_name,
        )
        set_exchange(exchange)

        ensure_dir(self.config.output_dir)
        self._prime_last_timestamps()

        self._thread = threading.Thread(target=self._run_loop, name="live-data-collector", daemon=True)
        self._thread.start()
        self._running = True
        self.state_cb("running")
        self._log(f"Collector started for account={self.account_name} exchange={self.exchange_name}")

    def pause(self) -> None:
        if not self._running:
            return
        self._pause_event.set()
        self.state_cb("paused")
        self._log("Collector paused")

    def resume(self) -> None:
        if not self._running:
            return
        self._pause_event.clear()
        self.state_cb("running")
        self._log("Collector resumed")

    def stop(self) -> None:
        if not self._running:
            return
        self._stop_event.set()
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        self._running = False
        self.state_cb("stopped")
        self._log("Collector stopped")

    def reconcile_missed_data(self) -> None:
        self._log("Reconciliation started")
        total_rows = 0
        for sym in self.config.symbols:
            total_rows += reconcile_trades_symbol(
                self.config.output_dir,
                sym,
                chunk_limit=self.config.reconcile_chunk_limit,
                log_cb=self._log,
            )
            for tf in self.config.timeframes:
                total_rows += reconcile_ohlcv_symbol_timeframe(
                    self.config.output_dir,
                    sym,
                    tf,
                    chunk_limit=self.config.reconcile_chunk_limit,
                    log_cb=self._log,
                )
        self._prime_last_timestamps()
        self._log(f"Reconciliation completed (+{total_rows} rows)")

    def _prime_last_timestamps(self) -> None:
        for sym in self.config.symbols:
            s = _safe_symbol(sym)
            trades_path = Path(self.config.output_dir) / "trades" / f"trades_{s}.csv"
            last_trade = last_numeric_value(trades_path, "timestamp_ms")
            if last_trade is not None:
                self._last_trade_ts[sym] = last_trade

            for tf in self.config.timeframes:
                ohlcv_path = Path(self.config.output_dir) / "ohlcv" / f"ohlcv_{s}_{tf}.csv"
                last_candle = last_numeric_value(ohlcv_path, "timestamp_ms")
                if last_candle is not None:
                    self._last_ohlcv_ts[(sym, tf)] = last_candle

    def _run_loop(self) -> None:
        try:
            while not self._stop_event.is_set():
                if self._pause_event.is_set():
                    time.sleep(0.25)
                    continue

                now = time.time()
                if now - self._last_polled["orders"] >= self.config.interval_orders_s:
                    self._collect_orders()
                    self._last_polled["orders"] = now

                if now - self._last_polled["orderbook"] >= self.config.interval_orderbook_s:
                    self._collect_orderbook()
                    self._last_polled["orderbook"] = now

                if now - self._last_polled["tickers"] >= self.config.interval_tickers_s:
                    self._collect_tickers()
                    self._last_polled["tickers"] = now

                if now - self._last_polled["trades"] >= self.config.interval_trades_s:
                    self._collect_trades()
                    self._last_polled["trades"] = now

                if now - self._last_polled["ohlcv"] >= self.config.interval_ohlcv_s:
                    self._collect_ohlcv()
                    self._last_polled["ohlcv"] = now

                # Close trade-aggregated bars when wall clock passes bar end (even if no new ticks this tick)
                self._flush_closed_trade_ohlcv()

                time.sleep(0.2)
        except Exception as e:
            self._log(f"Collector crashed: {e}")
            self.state_cb("error")
            self._running = False

    def _collect_orders(self) -> None:
        all_rows = []
        ts = _now_iso()
        for sym in self.config.symbols:
            orders = fetch_open_orders(sym, force_refresh=True)
            for o in orders:
                all_rows.append(
                    {
                        "collected_at_utc": ts,
                        "symbol": o.get("symbol", sym),
                        "side": o.get("side"),
                        "type": o.get("type"),
                        "amount": o.get("amount"),
                        "price": o.get("price"),
                        "status": o.get("status"),
                        "id": o.get("id"),
                        "raw_json": json.dumps(o, ensure_ascii=False),
                    }
                )
        n = append_rows_csv(
            Path(self.config.output_dir) / "orders" / "orders.csv",
            ["collected_at_utc", "symbol", "side", "type", "amount", "price", "status", "id", "raw_json"],
            all_rows,
        )
        if n:
            self._log(f"Collected orders (+{n})")

    def _collect_orderbook(self) -> None:
        rows = []
        ts = _now_iso()
        for sym in self.config.symbols:
            ob = fetch_order_book(sym, force_refresh=True)
            if not ob:
                continue
            bids = ob.get("bids") or []
            asks = ob.get("asks") or []
            best_bid = bids[0][0] if bids else None
            best_ask = asks[0][0] if asks else None
            bid_size = bids[0][1] if bids else None
            ask_size = asks[0][1] if asks else None
            spread_pct = None
            if best_bid and best_ask and (best_bid + best_ask) > 0:
                mid = (best_bid + best_ask) / 2.0
                spread_pct = ((best_ask - best_bid) / mid) * 100.0
            rows.append(
                {
                    "collected_at_utc": ts,
                    "symbol": sym,
                    "best_bid": best_bid,
                    "best_ask": best_ask,
                    "bid_size": bid_size,
                    "ask_size": ask_size,
                    "spread_pct": spread_pct,
                    "raw_json": json.dumps(ob, ensure_ascii=False),
                }
            )
        n = append_rows_csv(
            Path(self.config.output_dir) / "orderbook" / "orderbook.csv",
            ["collected_at_utc", "symbol", "best_bid", "best_ask", "bid_size", "ask_size", "spread_pct", "raw_json"],
            rows,
        )
        if n:
            self._log(f"Collected orderbook snapshots (+{n})")

    def _collect_tickers(self) -> None:
        tickers = fetch_tickers(self.config.symbols)
        rows = []
        ts = _now_iso()
        for sym in self.config.symbols:
            t = tickers.get(sym)
            if not isinstance(t, dict):
                continue
            rows.append(
                {
                    "collected_at_utc": ts,
                    "symbol": sym,
                    "last": t.get("last"),
                    "percentage": t.get("percentage"),
                    "quoteVolume": t.get("quoteVolume"),
                    "baseVolume": t.get("baseVolume"),
                    "raw_json": json.dumps(t, ensure_ascii=False),
                }
            )
        n = append_rows_csv(
            Path(self.config.output_dir) / "tickers" / "tickers.csv",
            ["collected_at_utc", "symbol", "last", "percentage", "quoteVolume", "baseVolume", "raw_json"],
            rows,
        )
        if n:
            self._log(f"Collected tickers (+{n})")

    def _collect_trades(self) -> None:
        for sym in self.config.symbols:
            last_seen = self._last_trade_ts.get(sym, 0)
            since_ms = int(last_seen) if last_seen and last_seen > 0 else None
            trades = fetch_trades(sym, since=since_ms, limit=self.config.trades_limit)
            if not trades:
                continue

            rows = []
            max_ts = last_seen
            for t in trades:
                try:
                    ts_ms = int(float(t.get("timestamp", 0) or 0))
                except Exception:
                    continue
                if ts_ms <= last_seen:
                    continue
                rows.append(
                    {
                        "timestamp_ms": ts_ms,
                        "symbol": str(t.get("symbol", sym) or sym),
                        "trade_id": str(t.get("id", "") or ""),
                        "side": str(t.get("side", "") or ""),
                        "price": float(t.get("price", 0.0) or 0.0),
                        "amount": float(t.get("amount", 0.0) or 0.0),
                        "cost": float(t.get("cost", 0.0) or 0.0),
                        "datetime": str(t.get("datetime", "") or ""),
                    }
                )
                if ts_ms > max_ts:
                    max_ts = ts_ms

            if not rows:
                continue

            n = append_rows_csv(
                Path(self.config.output_dir) / "trades" / f"trades_{_safe_symbol(sym)}.csv",
                ["timestamp_ms", "symbol", "trade_id", "side", "price", "amount", "cost", "datetime"],
                rows,
            )
            if n:
                self._last_trade_ts[sym] = max_ts
                self._log(f"Collected trades {sym} (+{n})")
                self._ingest_trades_for_ohlcv(sym, rows)

    def _ingest_trades_for_ohlcv(self, sym: str, trade_rows: list[dict]) -> None:
        """Roll ticks into per-timeframe accumulators (see ``trade_aggregate_timeframes`` in config)."""
        if not trade_rows:
            return
        sorted_rows = sorted(
            trade_rows,
            key=lambda r: int(float(r.get("timestamp_ms", 0) or 0)),
        )
        out_dir = Path(self.config.output_dir)
        for tf in self.config.trade_aggregate_timeframes:
            try:
                period_ms = timeframe_to_milliseconds(tf)
            except ValueError:
                self._log(f"Trade OHLCV skipped: unsupported timeframe {tf!r}")
                continue
            path = out_dir / "ohlcv" / f"ohlcv_trades_{_safe_symbol(sym)}_{tf}.csv"
            last_done_raw = last_numeric_value(path, "timestamp_ms")
            last_done = last_done_raw if last_done_raw is not None else -1
            filtered: list[dict] = []
            for r in sorted_rows:
                try:
                    ts_ms = int(float(r.get("timestamp_ms", 0) or 0))
                except (TypeError, ValueError):
                    continue
                if ts_ms <= 0:
                    continue
                b0 = bar_open_timestamp_ms(ts_ms, period_ms)
                if last_done >= 0 and b0 <= last_done:
                    continue
                filtered.append(r)
            if not filtered:
                continue
            key = (sym, tf)
            if key not in self._trade_ohlcv_accum:
                self._trade_ohlcv_accum[key] = TradeOhlcvAccumulator(period_ms=period_ms)
            self._trade_ohlcv_accum[key].ingest_sorted_trades(filtered)

    def _flush_closed_trade_ohlcv(self) -> None:
        """Append completed trade-aggregated bars to ``ohlcv/ohlcv_trades_*``."""
        wall_ms = int(time.time() * 1000)
        out_dir = Path(self.config.output_dir)
        fields = trade_ohlcv_csv_fieldnames()
        for key, acc in list(self._trade_ohlcv_accum.items()):
            sym, tf = key
            path = out_dir / "ohlcv" / f"ohlcv_trades_{_safe_symbol(sym)}_{tf}.csv"
            last_raw = last_numeric_value(path, "timestamp_ms")
            last_flushed = last_raw if last_raw is not None else -1
            closed = acc.pop_closed_bars(wall_ms, last_flushed)
            if not closed:
                continue
            rows_out = [
                {
                    "timestamp_ms": r["timestamp_ms"],
                    "symbol": sym,
                    "timeframe": tf,
                    "open": r["open"],
                    "high": r["high"],
                    "low": r["low"],
                    "close": r["close"],
                    "volume": r["volume"],
                    "trade_count": r["trade_count"],
                    "source": "trades",
                }
                for r in closed
            ]
            n = append_rows_csv(path, fields, rows_out)
            if n:
                self._log(f"Trade-aggregated OHLCV {sym} {tf} (+{n} bars)")

    def _collect_ohlcv(self) -> None:
        for sym in self.config.symbols:
            for tf in self.config.timeframes:
                df = fetch_ohlcv(sym, tf, limit=self.config.ohlcv_limit)
                if df is None or df.empty:
                    continue

                last_seen = self._last_ohlcv_ts.get((sym, tf), 0)
                rows = []
                max_ts = last_seen
                for _, row in df.iterrows():
                    ts_raw = row.get("timestamp")
                    try:
                        ts_ms = int(ts_raw.value // 10**6) if hasattr(ts_raw, "value") else int(float(ts_raw))
                    except Exception:
                        continue
                    if ts_ms <= last_seen:
                        continue
                    rows.append(
                        {
                            "timestamp_ms": ts_ms,
                            "symbol": sym,
                            "timeframe": tf,
                            "open": float(row.get("open", 0.0)),
                            "high": float(row.get("high", 0.0)),
                            "low": float(row.get("low", 0.0)),
                            "close": float(row.get("close", 0.0)),
                            "volume": float(row.get("volume", 0.0)),
                        }
                    )
                    if ts_ms > max_ts:
                        max_ts = ts_ms

                if not rows:
                    continue

                n = append_rows_csv(
                    Path(self.config.output_dir) / "ohlcv" / f"ohlcv_{_safe_symbol(sym)}_{tf}.csv",
                    ["timestamp_ms", "symbol", "timeframe", "open", "high", "low", "close", "volume"],
                    rows,
                )
                if n:
                    self._last_ohlcv_ts[(sym, tf)] = max_ts
                    self._log(f"Collected OHLCV {sym} {tf} (+{n})")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _safe_symbol(symbol: str) -> str:
    return symbol.replace("/", "_").replace(":", "_")
