"""Utility helpers for the Power BI API client."""

from __future__ import annotations

from typing import Dict, List

import requests
from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv()


def fetch_paginated(url: str, headers: Dict[str, str], top: int = 100) -> List[dict]:
    """Return all paginated results using $top and $skip parameters."""
    results: List[dict] = []
    skip = 0
    while True:
        delim = "?" if "?" not in url else "&"
        paged_url = f"{url}{delim}$top={top}&$skip={skip}"
        response = requests.get(paged_url, headers=headers)
        response.raise_for_status()
        data = response.json().get("value", [])
        results.extend(data)
        if len(data) < top:
            break
        skip += top
    return results
