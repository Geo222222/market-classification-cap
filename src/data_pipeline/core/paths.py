"""Paths resolved from the ``data_pipeline`` package location (not process cwd)."""

from __future__ import annotations

from pathlib import Path

# Directory containing app/, core/, services/, app_config.yaml, ...
_DATA_PIPELINE_ROOT = Path(__file__).resolve().parent.parent


def get_data_pipeline_root() -> Path:
    """Return ``.../src/data_pipeline`` (this package root)."""
    return _DATA_PIPELINE_ROOT


def get_repo_root() -> Path:
    """Return repository root (parent of ``src``) when layout is ``repo/src/data_pipeline``."""
    return _DATA_PIPELINE_ROOT.parent.parent


def resolve_under_package(path: str | Path) -> Path:
    """Resolve ``path``; if relative, it is relative to the package root."""
    p = Path(path)
    if p.is_absolute():
        return p.resolve()
    return (_DATA_PIPELINE_ROOT / p).resolve()


def resolve_config_path(path: str | Path | None) -> Path:
    """Resolve config file path; default is ``app_config.yaml`` next to this package."""
    if path is None:
        return (_DATA_PIPELINE_ROOT / "app_config.yaml").resolve()
    p = Path(path)
    if p.is_absolute():
        return p.resolve()
    return (_DATA_PIPELINE_ROOT / p).resolve()


def resolve_credentials_path() -> Path:
    """Find ``credentials.yaml`` without relying on cwd."""
    candidates = [
        _DATA_PIPELINE_ROOT / "credentials.yaml",
        get_repo_root() / "credentials.yaml",
        _DATA_PIPELINE_ROOT / "me3 - Copy" / "credentials.yaml",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate.resolve()
    searched = ", ".join(str(c) for c in candidates)
    raise FileNotFoundError(
        "credentials.yaml not found. Tried: " + searched
    )
