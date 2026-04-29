import pytest

from france_travail import BadRequestError, ServerError

_OFFRE_ID = "048KLTP"
_BASE_URL = "https://api.francetravail.io/partenaire/offresdemploi/v2/offres"


def test_get_offre_200_returns_offre(client, httpx_mock, sample_offre):
    httpx_mock.add_response(json=sample_offre)
    offre = client.get_offre(_OFFRE_ID)
    assert offre is not None
    assert offre.id == _OFFRE_ID
    assert offre.intitule == "Boulanger / Boulangère (H/F)"


def test_get_offre_204_returns_none(client, httpx_mock):
    httpx_mock.add_response(status_code=204)
    assert client.get_offre(_OFFRE_ID) is None


def test_get_offre_400_raises_bad_request(client, httpx_mock):
    httpx_mock.add_response(status_code=400, text="Bad request")
    with pytest.raises(BadRequestError) as exc_info:
        client.get_offre(_OFFRE_ID)
    assert exc_info.value.status_code == 400


def test_get_offre_500_raises_server_error(client, httpx_mock):
    httpx_mock.add_response(status_code=500)
    with pytest.raises(ServerError) as exc_info:
        client.get_offre(_OFFRE_ID)
    assert exc_info.value.status_code == 500


def test_get_offre_hits_correct_url(client, httpx_mock, sample_offre):
    httpx_mock.add_response(json=sample_offre)
    client.get_offre(_OFFRE_ID)
    request = httpx_mock.get_requests()[0]
    assert str(request.url) == f"{_BASE_URL}/{_OFFRE_ID}"
