"""Exchange bootstrap for standalone collector app."""

from __future__ import annotations

import ccxt
import yaml

from ..core.errors import normalize_exchange_name
from ..core.paths import resolve_credentials_path


def _load_account(account_name: str = "") -> tuple[str, str, str, str]:
    path = resolve_credentials_path()
    with path.open("r", encoding="utf-8") as f:
        creds = yaml.safe_load(f) or {}

    accounts = creds.get("accounts", []) if isinstance(creds, dict) else []
    if not isinstance(accounts, list) or not accounts:
        raise ValueError("No accounts found in credentials.yaml")

    selected = None
    if account_name:
        for acc in accounts:
            if str(acc.get("name", "")).strip().lower() == account_name.strip().lower():
                selected = acc
                break

    if selected is None:
        for acc in accounts:
            if str(acc.get("name", "")).strip().upper() == "EPX":
                selected = acc
                break

    if selected is None:
        default_name = str(creds.get("default_account", "") or "")
        if default_name:
            for acc in accounts:
                if str(acc.get("name", "")) == default_name:
                    selected = acc
                    break

    if selected is None:
        selected = accounts[0]

    exch = normalize_exchange_name(selected.get("exchange", "htx"))
    key = str(selected.get("api_key", "") or "")
    secret = str(selected.get("secret_key", "") or "")
    name = str(selected.get("name", "") or "")
    if not key or not secret:
        raise ValueError(f"Missing API key/secret for account '{name}'")
    return name, exch, key, secret


def create_exchange(account_name: str = "", exchange_name_override: str = ""):
    """Create and load CCXT exchange instance from credentials."""
    name, exchange_name, api_key, secret_key = _load_account(account_name=account_name)
    if exchange_name_override:
        exchange_name = normalize_exchange_name(exchange_name_override)

    if not hasattr(ccxt, exchange_name):
        raise ValueError(f"Unsupported exchange: {exchange_name}")

    exchange_cls = getattr(ccxt, exchange_name)
    exchange = exchange_cls(
        {
            "apiKey": api_key,
            "secret": secret_key,
            "enableRateLimit": True,
            "timeout": 20000,
            "options": {"defaultType": "swap"},
        }
    )

    # Match existing runtime behavior for HTX endpoints.
    try:
        if hasattr(exchange, "session") and exchange_name in {"htx", "huobi"}:
            exchange.session.verify = False
    except Exception:
        pass

    exchange.load_markets()
    return name, exchange_name, exchange
