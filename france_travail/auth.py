import time

import httpx

from .exceptions import AuthenticationError

_TOKEN_URL = "https://entreprise.francetravail.fr/connexion/oauth2/access_token"
_SCOPES = "o2dsoffre api_offresdemploiv2"


class OAuth2TokenManager:
    def __init__(self, client_id: str, client_secret: str, http: httpx.Client):
        self._client_id = client_id
        self._client_secret = client_secret
        self._http = http
        self._token: str | None = None
        self._expires_at: float = 0.0

    def get_token(self) -> str:
        if self._token and time.monotonic() < self._expires_at - 30:
            return self._token
        return self._refresh()

    def _refresh(self) -> str:
        try:
            response = self._http.post(
                _TOKEN_URL,
                params={"realm": "/partenaire"},
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "scope": _SCOPES,
                },
            )
        except httpx.RequestError as e:
            raise AuthenticationError(f"Erreur réseau lors de l'authentification : {e}") from e

        if response.status_code != 200:
            raise AuthenticationError(
                f"Échec de l'authentification : {response.text}",
                status_code=response.status_code,
            )
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.monotonic() + data.get("expires_in", 1500)
        return self._token
