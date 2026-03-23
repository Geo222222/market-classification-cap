"""Shared runtime state for project exchange functions."""

from __future__ import annotations

from typing import Any

EXCHANGE: Any = None

order_cache = {
    "data": {},
    "timestamp": 0.0,
    "ttl": 30.0,
}

orderbook_cache = {
    "data": {},
    "timestamp": 0.0,
    "ttl": 5.0,
}


def set_exchange(exchange: Any) -> None:
    """Set exchange instance used by all project modules."""
    global EXCHANGE
    EXCHANGE = exchange


def get_exchange() -> Any:
    """Return current exchange instance."""
    return EXCHANGE


def reset_caches() -> None:
    """Reset all runtime caches."""
    order_cache["data"] = {}
    order_cache["timestamp"] = 0.0

    orderbook_cache["data"] = {}
    orderbook_cache["timestamp"] = 0.0
