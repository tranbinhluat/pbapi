"""Utility helpers for the Power BI API client."""

from __future__ import annotations

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv()
