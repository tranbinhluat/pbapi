"""Utility helpers for the Power BI API client."""

from __future__ import annotations

from dotenv import load_dotenv
import requests
import time
from typing import List, Dict

from .auth import PowerBIAuth


def load_env() -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv()


def fetch_paginated(
    url: str,
    auth: PowerBIAuth,
    page_size: int = 5000,
    sleep: float | int = 0,
) -> List[Dict]:
    """Fetch all items from a paginated Power BI endpoint.

    Parameters
    ----------
    url:
        Endpoint URL to query.
    auth:
        Auth handler providing headers.
    page_size:
        Maximum number of records per request.
    sleep:
        Seconds to wait between requests.
    """

    results: List[Dict] = []
    skip = 0
    while True:
        params = {"$top": page_size, "$skip": skip}
        response = requests.get(url, headers=auth.headers(), params=params)
        response.raise_for_status()
        chunk = response.json().get("value", [])
        results.extend(chunk)
        if len(chunk) < page_size:
            break
        skip += page_size
        if sleep:
            time.sleep(sleep)
    return results
