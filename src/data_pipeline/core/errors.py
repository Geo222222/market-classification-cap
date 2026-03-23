"""Error classification helpers for exchange API calls."""

from __future__ import annotations


def normalize_exchange_name(name: str | None) -> str:
    """Normalize exchange name for HTX migration compatibility."""
    if name and name.lower() == "huobi":
        return "htx"
    return name.lower() if name else "htx"


def is_htx_endpoint_error(error: Exception | str) -> bool:
    """Return True if error likely indicates HTX endpoint/network outage."""
    s = str(error or "").lower()
    is_htxish = any(h in s for h in (
        "api.hbdm.com",
        "hbdm.com",
        "api.htx.com",
        "htx ",
        "huobi",
        "linear-swap",
        "swap",
        "contract_code=",
        "swap_contract_info",
    ))
    if not is_htxish:
        return False

    symptoms = (
        "timed out",
        "timeout",
        "max retries exceeded",
        "connection refused",
        "connection reset",
        "connection aborted",
        "remote end closed connection",
        "remote disconnected",
        "name or service not known",
        "no address associated with hostname",
        "temporary failure in name resolution",
        "ssl",
        "certificate verify failed",
        "tls",
        "bad gateway",
        "gateway time-out",
        "gateway timeout",
        "service unavailable",
        "http 502",
        "http 503",
        "http 504",
        "status code 502",
        "status code 503",
        "status code 504",
        "httpconnectionpool",
        "read timed out",
    )
    return any(x in s for x in symptoms)


def handle_api_error(error: Exception | str, function_name: str = "API") -> bool:
    """Log API errors and return whether it was classified as HTX endpoint issue."""
    if is_htx_endpoint_error(error):
        print(f"{function_name}: Endpoint error (live mode retained) - {error}")
        return True
    print(f"{function_name}: Error - {error}")
    return False
