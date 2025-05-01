"""
OddsAPI client package for The Odds API - a sports odds API.

This package provides an async client for interacting with The Odds API v4.
"""
from .server import (
    get_odds,
    get_event_odds,
    get_events,
)

__all__ = [
    "get_odds",
    "get_event_odds",
    "get_events",
]