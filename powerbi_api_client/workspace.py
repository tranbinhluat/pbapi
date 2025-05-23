"""Workspace interactions with the Power BI API."""

from __future__ import annotations

import requests
import pandas as pd

from .auth import PowerBIAuth


class Workspace:
    """Fetch and process Power BI workspaces."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth) -> None:
        self.auth = auth

    def get_raw(self) -> list[dict]:
        """Return raw workspace JSON objects."""
        url = f"{self.BASE_URL}/groups"
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self) -> pd.DataFrame:
        """Return workspace information as a pandas DataFrame."""
        data = self.get_raw()
        return pd.DataFrame(data)
