"""Data model interactions for datasets."""

from __future__ import annotations

import requests
import pandas as pd

from .utils import fetch_paginated

from .auth import PowerBIAuth


class DataModel:
    """Fetch tables within a dataset."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth, workspace_id: str, dataset_id: str) -> None:
        self.auth = auth
        self.workspace_id = workspace_id
        self.dataset_id = dataset_id

    def get_raw(self, fetch_all: bool = False) -> list[dict]:
        """Return tables inside the dataset.

        Parameters
        ----------
        fetch_all:
            When ``True``, paginate through all tables with ``$top`` and
            ``$skip``.
        """
        url = (
            f"{self.BASE_URL}/groups/{self.workspace_id}/datasets/{self.dataset_id}/tables"
        )
        if fetch_all:
            return fetch_paginated(url, self.auth.headers())
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self) -> pd.DataFrame:
        """Return tables as a DataFrame."""
        data = self.get_raw()
        return pd.DataFrame(data)
