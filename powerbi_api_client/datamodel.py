"""Data model interactions for datasets."""

from __future__ import annotations

import requests
import pandas as pd

from .auth import PowerBIAuth


class DataModel:
    """Fetch tables within a dataset."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth, workspace_id: str, dataset_id: str) -> None:
        self.auth = auth
        self.workspace_id = workspace_id
        self.dataset_id = dataset_id

    def get_raw(self) -> list[dict]:
        """Return tables inside the dataset."""
        url = f"{self.BASE_URL}/groups/{self.workspace_id}/datasets/{self.dataset_id}/tables"
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self) -> pd.DataFrame:
        """Return tables as a DataFrame."""
        data = self.get_raw()
        return pd.DataFrame(data)
