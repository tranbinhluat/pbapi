"""Authentication utilities for Power BI API."""

from __future__ import annotations

import os
from typing import Optional, Dict

from dotenv import load_dotenv
import msal


class PowerBIAuth:
    """Handle authentication with Azure AD for Power BI."""

    def __init__(
        self,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        scope: Optional[str] = None,
    ) -> None:
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope or "https://analysis.windows.net/powerbi/api/.default"
        self._token: Optional[Dict[str, str]] = None
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.app = msal.ConfidentialClientApplication(
            client_id=self.client_id,
            authority=authority,
            client_credential=self.client_secret,
        )

    @classmethod
    def from_env(cls) -> "PowerBIAuth":
        """Create an auth handler using environment variables."""
        load_dotenv()
        tenant_id = os.getenv("POWERBI_TENANT_ID")
        client_id = os.getenv("POWERBI_CLIENT_ID")
        client_secret = os.getenv("POWERBI_CLIENT_SECRET")
        if not all([tenant_id, client_id, client_secret]):
            raise ValueError(
                "Missing required environment variables: POWERBI_TENANT_ID, POWERBI_CLIENT_ID, POWERBI_CLIENT_SECRET"
            )
        return cls(tenant_id, client_id, client_secret)

    def get_access_token(self) -> str:
        """Return a valid access token."""
        if not self._token or "access_token" not in self._token:
            self._token = self.app.acquire_token_for_client(scopes=[self.scope])
            if "access_token" not in self._token:
                raise RuntimeError(f"Failed to obtain token: {self._token.get('error_description')}")
        return self._token["access_token"]

    def headers(self) -> Dict[str, str]:
        """Return standard headers for API calls."""
        return {
            "Authorization": f"Bearer {self.get_access_token()}",
            "Content-Type": "application/json",
        }
