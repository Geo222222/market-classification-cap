#!/usr/bin/env python3
"""
Launch the live data collector UI without running `pip install -e .`.

Usage (from repository root):
    python run_collector.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from data_pipeline.main import run  # noqa: E402

if __name__ == "__main__":
    run()  # stub prints instructions until package is rebuilt
