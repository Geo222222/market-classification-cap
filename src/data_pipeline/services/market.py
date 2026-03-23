"""Live-only market data helpers."""

from __future__ import annotations

import time

import pandas as pd

from ..core.cleaning import (
    clean_ohlcv_df,
    clean_order_book,
    clean_ticker,
    clean_tickers,
    clean_trades,
)
from ..core.context import get_exchange, orderbook_cache
from ..core.errors import handle_api_error, is_htx_endpoint_error


def fetch_ohlcv(symbol: str, timeframe: str, limit: int = 100, since: int | None = None):
    """Fetch live OHLCV and return a normalized DataFrame."""
    try:
        exchange = get_exchange()
        if exchange is None:
            print("OHLCV API: No exchange available")
            return None

        max_retries = 3
        retry_delay = 0.5

        for attempt in range(max_retries):
            try:
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=limit)
                if not ohlcv:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return None

                df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

                return clean_ohlcv_df(df)
            except Exception:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"OHLCV API: Failed after {max_retries} attempts")
                    return None
    except Exception as e:
        print(f"OHLCV API: Critical error fetching OHLCV data: {e}")
        return None


def fetch_trades(symbol: str, since: int | None = None, limit: int = 100) -> list:
    """Fetch live trades."""
    try:
        exchange = get_exchange()
        if exchange is None:
            return []
        trades = exchange.fetch_trades(symbol, since=since, limit=limit)
        return clean_trades(trades)
    except Exception as e:
        print(f"TRADES API: Error fetching trades: {e}")
        return []


def fetch_ticker(symbol: str):
    """Fetch live ticker for one symbol."""
    try:
        exchange = get_exchange()
        if exchange is None:
            return None
        try:
            return clean_ticker(exchange.fetch_ticker(symbol))
        except Exception as e:
            if is_htx_endpoint_error(e):
                handle_api_error(e, "TICKER API")
            else:
                print(f"TICKER API: Error fetching ticker for {symbol}: {e}")
            return None
    except Exception as e:
        print(f"TICKER API: Error in fetch_ticker: {e}")
        return None


def fetch_tickers(symbols: list[str] | None = None) -> dict:
    """Fetch live tickers for specific symbols or all."""
    try:
        exchange = get_exchange()
        if exchange is None:
            return {}
        if symbols:
            out: dict = {}
            for symbol in symbols:
                try:
                    cleaned = clean_ticker(exchange.fetch_ticker(symbol))
                    if cleaned is not None:
                        out[symbol] = cleaned
                except Exception as e:
                    print(f"TICKERS API: Error fetching ticker for {symbol}: {e}")
            return out
        return clean_tickers(exchange.fetch_tickers())
    except Exception as e:
        print(f"TICKERS API: Error fetching tickers: {e}")
        return {}


def fetch_order_book(symbol: str, force_refresh: bool = False):
    """Fetch live order book with cache."""
    try:
        exchange = get_exchange()
        current_time = time.time()

        if (not force_refresh) and symbol in orderbook_cache["data"]:
            cache_age = current_time - float(orderbook_cache["timestamp"])
            if cache_age < float(orderbook_cache["ttl"]):
                return clean_order_book(orderbook_cache["data"][symbol])

        if exchange is None:
            print("ORDERBOOK API: No exchange available")
            return None

        try:
            order_book = exchange.fetch_order_book(symbol)
            orderbook_cache["data"][symbol] = order_book
            orderbook_cache["timestamp"] = current_time
            return clean_order_book(order_book)
        except Exception as e:
            if is_htx_endpoint_error(e):
                handle_api_error(e, "ORDERBOOK API")
            else:
                print(f"ORDERBOOK API: Error fetching order book: {e}")
            return None
    except Exception as e:
        if is_htx_endpoint_error(e):
            handle_api_error(e, "ORDERBOOK API")
            return None
        print(f"ORDERBOOK API: Error fetching order book: {e}")
        return None


def fetch_best_bid(symbol: str):
    """Fetch top bid from live orderbook."""
    try:
        order_book = fetch_order_book(symbol)
        if order_book and "bids" in order_book and order_book["bids"]:
            return order_book["bids"][0][0]
        return None
    except Exception as e:
        print(f"ORDERBOOK API: Error fetching best bid: {e}")
        return None


def fetch_best_ask(symbol: str):
    """Fetch top ask from live orderbook."""
    try:
        order_book = fetch_order_book(symbol)
        if order_book and "asks" in order_book and order_book["asks"]:
            return order_book["asks"][0][0]
        return None
    except Exception as e:
        print(f"ORDERBOOK API: Error fetching best ask: {e}")
        return None
