"""Minimal Tk UI for collector pause/resume/stop and reconciliation."""

from __future__ import annotations

import csv
import queue
import threading
import tkinter as tk
from datetime import datetime, timezone
from pathlib import Path
from tkinter import messagebox, scrolledtext, ttk

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ..app.collector import LiveDataCollector
from ..core.config import AppConfig


class CollectorApp(tk.Tk):
    def __init__(self, config: AppConfig):
        super().__init__()
        self.title("Project Live Collector")
        self.geometry("1180x680")

        self.config_obj = config
        self._log_queue: "queue.Queue[str]" = queue.Queue()
        self._state_var = tk.StringVar(value="stopped")
        self._chart_symbol_var = tk.StringVar(value=self.config_obj.symbols[0])
        self._chart_timeframe_var = tk.StringVar(value=self.config_obj.timeframes[0])
        self._chart_metric_var = tk.StringVar(value="OHLCV Close")
        self._chart_last_error = None

        self.collector = LiveDataCollector(config, log_cb=self._enqueue_log, state_cb=self._set_state)

        self._build_ui()
        self.after(120, self._drain_logs)
        self.after(1500, self._refresh_chart)

    def _build_ui(self) -> None:
        top = ttk.Frame(self)
        top.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(top, text="State:").pack(side=tk.LEFT)
        ttk.Label(top, textvariable=self._state_var).pack(side=tk.LEFT, padx=(4, 20))

        ttk.Button(top, text="Start", command=self._start).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Pause", command=self._pause).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Resume", command=self._resume).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Stop", command=self._stop).pack(side=tk.LEFT, padx=4)
        ttk.Button(top, text="Reconcile", command=self._reconcile).pack(side=tk.LEFT, padx=12)

        info = ttk.Label(
            self,
            text=(
                f"Symbols: {', '.join(self.config_obj.symbols)} | "
                f"Timeframes: {', '.join(self.config_obj.timeframes)} | "
                f"CSV Output: {Path(self.config_obj.output_dir).resolve()}"
            ),
        )
        info.pack(fill=tk.X, padx=10)

        body = ttk.Panedwindow(self, orient=tk.HORIZONTAL)
        body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        log_frame = ttk.Frame(body)
        chart_frame = ttk.Frame(body)
        body.add(log_frame, weight=3)
        body.add(chart_frame, weight=2)

        self.log_box = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=24)
        self.log_box.pack(fill=tk.BOTH, expand=True)
        self.log_box.configure(state=tk.DISABLED)

        chart_controls = ttk.Frame(chart_frame)
        chart_controls.pack(fill=tk.X, pady=(0, 6))

        ttk.Label(chart_controls, text="Chart:").pack(side=tk.LEFT)
        self.chart_metric_cb = ttk.Combobox(
            chart_controls,
            textvariable=self._chart_metric_var,
            values=["OHLCV Close", "Trades Price", "Orderbook Spread %"],
            state="readonly",
            width=18,
        )
        self.chart_metric_cb.pack(side=tk.LEFT, padx=4)

        ttk.Label(chart_controls, text="Symbol:").pack(side=tk.LEFT, padx=(10, 0))
        self.chart_symbol_cb = ttk.Combobox(
            chart_controls,
            textvariable=self._chart_symbol_var,
            values=self.config_obj.symbols,
            state="readonly",
            width=18,
        )
        self.chart_symbol_cb.pack(side=tk.LEFT, padx=4)

        ttk.Label(chart_controls, text="TF:").pack(side=tk.LEFT, padx=(10, 0))
        self.chart_tf_cb = ttk.Combobox(
            chart_controls,
            textvariable=self._chart_timeframe_var,
            values=self.config_obj.timeframes,
            state="readonly",
            width=8,
        )
        self.chart_tf_cb.pack(side=tk.LEFT, padx=4)

        self.fig = Figure(figsize=(5.6, 4.8), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title("Live CSV Chart")
        self.ax.grid(alpha=0.3)

        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw_idle()

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _enqueue_log(self, msg: str) -> None:
        self._log_queue.put(msg)

    def _set_state(self, state: str) -> None:
        self._state_var.set(state)

    def _drain_logs(self) -> None:
        try:
            while True:
                msg = self._log_queue.get_nowait()
                self.log_box.configure(state=tk.NORMAL)
                self.log_box.insert(tk.END, msg + "\n")
                self.log_box.see(tk.END)
                self.log_box.configure(state=tk.DISABLED)
        except queue.Empty:
            pass
        self.after(120, self._drain_logs)

    def _start(self) -> None:
        try:
            self.collector.start()
        except Exception as e:
            messagebox.showerror("Start Error", str(e))

    def _pause(self) -> None:
        self.collector.pause()

    def _resume(self) -> None:
        self.collector.resume()

    def _stop(self) -> None:
        self.collector.stop()

    def _reconcile(self) -> None:
        def _job():
            try:
                self.collector.reconcile_missed_data()
            except Exception as e:
                self._enqueue_log(f"Reconcile error: {e}")

        threading.Thread(target=_job, daemon=True).start()

    def _safe_symbol(self, symbol: str) -> str:
        return str(symbol).replace("/", "_").replace(":", "_")

    def _read_csv_rows(self, path: Path, limit: int = 300) -> list[dict]:
        if not path.exists():
            return []
        try:
            with path.open("r", newline="", encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            if limit > 0 and len(rows) > limit:
                rows = rows[-limit:]
            return rows
        except Exception:
            return []

    def _plot_ohlcv_close(self, symbol: str, timeframe: str) -> None:
        safe = self._safe_symbol(symbol)
        p = Path(self.config_obj.output_dir) / "ohlcv" / f"ohlcv_{safe}_{timeframe}.csv"
        rows = self._read_csv_rows(p, limit=500)
        xs = []
        ys = []
        for r in rows:
            try:
                ts_ms = int(float(r.get("timestamp_ms", 0) or 0))
                close = float(r.get("close", 0) or 0)
            except Exception:
                continue
            if ts_ms <= 0:
                continue
            xs.append(datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc))
            ys.append(close)

        self.ax.clear()
        self.ax.grid(alpha=0.3)
        self.ax.set_title(f"{symbol} {timeframe} Close (CSV)")
        if xs and ys:
            self.ax.plot(xs, ys, linewidth=1.4, color="#1565c0")
            self.ax.set_ylabel("Close")
        else:
            self.ax.text(0.5, 0.5, "No OHLCV rows yet", ha="center", va="center", transform=self.ax.transAxes)

    def _plot_trades_price(self, symbol: str) -> None:
        safe = self._safe_symbol(symbol)
        p = Path(self.config_obj.output_dir) / "trades" / f"trades_{safe}.csv"
        rows = self._read_csv_rows(p, limit=500)
        xs = []
        ys = []
        for r in rows:
            try:
                ts_ms = int(float(r.get("timestamp_ms", 0) or 0))
                price = float(r.get("price", 0) or 0)
            except Exception:
                continue
            if ts_ms <= 0:
                continue
            xs.append(datetime.fromtimestamp(ts_ms / 1000.0, tz=timezone.utc))
            ys.append(price)

        self.ax.clear()
        self.ax.grid(alpha=0.3)
        self.ax.set_title(f"{symbol} Trades Price (CSV)")
        if xs and ys:
            self.ax.plot(xs, ys, linewidth=1.1, color="#2e7d32")
            self.ax.set_ylabel("Price")
        else:
            self.ax.text(0.5, 0.5, "No trades rows yet", ha="center", va="center", transform=self.ax.transAxes)

    def _plot_orderbook_spread(self, symbol: str) -> None:
        p = Path(self.config_obj.output_dir) / "orderbook" / "orderbook.csv"
        rows = self._read_csv_rows(p, limit=700)
        xs = []
        ys = []
        for r in rows:
            if str(r.get("symbol", "")) != symbol:
                continue
            try:
                spread = float(r.get("spread_pct", 0) or 0)
                ts_text = str(r.get("collected_at_utc", "") or "")
                ts = datetime.strptime(ts_text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            except Exception:
                continue
            xs.append(ts)
            ys.append(spread)

        self.ax.clear()
        self.ax.grid(alpha=0.3)
        self.ax.set_title(f"{symbol} Orderbook Spread % (CSV)")
        if xs and ys:
            self.ax.plot(xs, ys, linewidth=1.1, color="#6a1b9a")
            self.ax.set_ylabel("Spread %")
        else:
            self.ax.text(0.5, 0.5, "No orderbook rows yet", ha="center", va="center", transform=self.ax.transAxes)

    def _refresh_chart(self) -> None:
        try:
            symbol = self._chart_symbol_var.get().strip()
            timeframe = self._chart_timeframe_var.get().strip()
            metric = self._chart_metric_var.get().strip()

            if metric == "OHLCV Close":
                self._plot_ohlcv_close(symbol, timeframe)
            elif metric == "Trades Price":
                self._plot_trades_price(symbol)
            else:
                self._plot_orderbook_spread(symbol)
            self.fig.autofmt_xdate()
            self.canvas.draw_idle()
            self._chart_last_error = None
        except Exception as e:
            if self._chart_last_error != str(e):
                self._enqueue_log(f"Chart refresh error: {e}")
                self._chart_last_error = str(e)
        finally:
            if self.winfo_exists():
                self.after(1500, self._refresh_chart)

    def _on_close(self) -> None:
        try:
            self.collector.stop()
        except Exception:
            pass
        self.destroy()
