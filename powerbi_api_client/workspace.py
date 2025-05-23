"""Workspace interactions with the Power BI API."""

from __future__ import annotations

import requests
import pandas as pd

from .utils import fetch_paginated

from .auth import PowerBIAuth


class Workspace:
    """Fetch and process Power BI workspaces."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth) -> None:
        self.auth = auth

    def get_raw(self, fetch_all: bool = False) -> list[dict]:
        """Return raw workspace JSON objects.

        Parameters
        ----------
        fetch_all:
            When ``True``, paginate through all workspaces using ``$top`` and
            ``$skip`` query parameters.
        """
        url = f"{self.BASE_URL}/groups"
        if fetch_all:
            return fetch_paginated(url, self.auth.headers())
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self) -> pd.DataFrame:
        """Return workspace information as a pandas DataFrame."""
        data = self.get_raw()
        return pd.DataFrame(data)
