"""Shared setup for the FastF1 plotting experiments."""

from pathlib import Path

import fastf1


def enable_cache():
    """Create and enable a repository-local cache, independent of cwd."""
    cache_dir = Path(__file__).resolve().parent / "Cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(cache_dir))
    return cache_dir
