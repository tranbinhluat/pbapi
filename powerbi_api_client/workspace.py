"""Workspace interactions with the Power BI API."""

from __future__ import annotations

import requests
import pandas as pd
from typing import List, Dict

from .auth import PowerBIAuth
from .utils import fetch_paginated


class Workspace:
    """Fetch and process Power BI workspaces."""

    BASE_URL = "https://api.powerbi.com/v1.0/myorg"

    def __init__(self, auth: PowerBIAuth) -> None:
        self.auth = auth

    def get_raw(self, fetch_all: bool = False, sleep: float | int = 0) -> List[Dict]:
        """Return raw workspace JSON objects.

        Parameters
        ----------
        fetch_all:
            If True, fetch all paginated results.
        sleep:
            Seconds to wait between paginated requests.
        """

        url = f"{self.BASE_URL}/groups"
        if fetch_all:
            return fetch_paginated(url, self.auth, sleep=sleep)
        response = requests.get(url, headers=self.auth.headers())
        response.raise_for_status()
        return response.json().get("value", [])

    def to_dataframe(self, fetch_all: bool = False, sleep: float | int = 0) -> pd.DataFrame:
        """Return workspace information as a pandas DataFrame.

        Parameters
        ----------
        fetch_all:
            If True, fetch all paginated results.
        sleep:
            Seconds to wait between paginated requests.
        """

        data = self.get_raw(fetch_all=fetch_all, sleep=sleep)
        return pd.DataFrame(data)
