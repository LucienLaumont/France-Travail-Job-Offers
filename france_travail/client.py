import time

import httpx

from .auth import OAuth2TokenManager
from .exceptions import BadRequestError, FranceTravailError, RateLimitError, ServerError
from .models import SearchResult
from .search_params import SearchParams

_SEARCH_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres/search"
_MAX_REQUESTS_PER_SECOND = 10


class FranceTravailClient:
    def __init__(self, client_id: str, client_secret: str):
        self._auth = OAuth2TokenManager(client_id, client_secret)
        self._http = httpx.Client(timeout=30.0)
        self._request_timestamps: list[float] = []

    def _wait_for_rate_limit(self) -> None:
        now = time.monotonic()
        self._request_timestamps = [t for t in self._request_timestamps if now - t < 1.0]
        if len(self._request_timestamps) >= _MAX_REQUESTS_PER_SECOND:
            sleep_duration = 1.0 - (now - self._request_timestamps[0])
            if sleep_duration > 0:
                time.sleep(sleep_duration)
        self._request_timestamps.append(time.monotonic())

    def search(self, params: SearchParams | None = None) -> SearchResult:
        self._wait_for_rate_limit()
        token = self._auth.get_token()
        query = params.to_query_dict() if params else {}
        response = self._http.get(
            _SEARCH_URL,
            headers={"Authorization": f"Bearer {token}"},
            params=query,
        )

        if response.status_code == 204:
            return SearchResult()

        if response.status_code == 400:
            raise BadRequestError(response.text, status_code=400)

        if response.status_code == 429:
            raise RateLimitError("Limite de taux dépassée (10 req/s)", status_code=429)

        if response.status_code == 500:
            raise ServerError("Erreur interne au serveur France Travail", status_code=500)

        if response.status_code not in (200, 206):
            raise FranceTravailError(
                f"Réponse inattendue : {response.status_code} — {response.text}",
                status_code=response.status_code,
            )

        data = response.json()
        result = SearchResult.model_validate(data)
        result.has_more = response.status_code == 206
        return result

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> "FranceTravailClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
