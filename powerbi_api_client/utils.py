"""Utility helpers for the Power BI API client."""

from __future__ import annotations

from typing import Any, Dict, List

import json
from pathlib import Path

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


def save_json(data: Any, file_name: str, folder: str = "json_data") -> str:
    """Write the provided data to a JSON file.

    The target directory will be created if it does not already exist.

    Parameters
    ----------
    data:
        Python object serialisable by ``json``.
    file_name:
        File name for the JSON output.
    folder:
        Directory in which to store the JSON file.

    Returns
    -------
    str
        The path to the written file.
    """

    directory = Path(folder)
    directory.mkdir(parents=True, exist_ok=True)
    file_path = directory / file_name
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(file_path)
