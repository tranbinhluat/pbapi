"""Dataset interactions with the Power BI API."""

from __future__ import annotations

import requests
import pandas as pd

from .auth import PowerBIAuth


class Dataset:
    """Fetch datasets for a workspace."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth, workspace_id: str) -> None:
        self.auth = auth
        self.workspace_id = workspace_id

    def get_raw(self) -> list[dict]:
        """Return datasets within the workspace."""
        url = f"{self.BASE_URL}/groups/{self.workspace_id}/datasets"
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self) -> pd.DataFrame:
        """Return datasets as a DataFrame."""
        data = self.get_raw()
        return pd.DataFrame(data)
