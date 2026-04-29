import time

import pytest

from france_travail import FranceTravailClient


@pytest.fixture
def token() -> str:
    return "test-access-token"


@pytest.fixture
def token_response(token: str) -> dict:
    return {"access_token": token, "token_type": "Bearer", "expires_in": 1500}


@pytest.fixture
def sample_offre() -> dict:
    return {
        "id": "048KLTP",
        "intitule": "Boulanger / Boulangère (H/F)",
        "typeContrat": "CDD",
        "lieuTravail": {"libelle": "74 - ANNECY", "codePostal": "74000"},
        "entreprise": {"nom": "Le boulanger austral"},
        "salaire": {"libelle": "Mensuel de 1923.00 Euros sur 12 mois"},
    }


@pytest.fixture
def sample_search_result(sample_offre: dict) -> dict:
    return {"resultats": [sample_offre], "filtresPossibles": []}


@pytest.fixture
def client(httpx_mock, token: str) -> FranceTravailClient:
    """Client avec token pré-chargé — aucun appel auth ne sera fait."""
    c = FranceTravailClient("test-client-id", "test-secret")
    c._auth._token = token
    c._auth._expires_at = time.monotonic() + 3600
    return c
