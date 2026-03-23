"""Live-only open-order helpers."""

from __future__ import annotations

import time

from ..core.cleaning import clean_orders
from ..core.context import get_exchange, order_cache


def fetch_open_orders(symbol: str | None = None, force_refresh: bool = False) -> list:
    """Fetch live open orders with per-symbol cache."""
    try:
        exchange = get_exchange()
        current_time = time.time()

        if (not force_refresh) and symbol in order_cache["data"]:
            cache_age = current_time - float(order_cache["timestamp"])
            if cache_age < float(order_cache["ttl"]):
                return clean_orders(order_cache["data"][symbol])

        if exchange is None:
            print("ORDERS API: Exchange is None")
            return []

        orders = exchange.fetch_open_orders(symbol)

        if symbol:
            order_cache["data"][symbol] = orders
            order_cache["timestamp"] = current_time

        return clean_orders(orders)
    except Exception as e:
        print(f"ORDERS API: Error fetching open orders: {e}")
        return []
