import httpx
import pytest

from france_travail import BadRequestError, FranceTravailError, SearchParams, ServerError


def test_search_200_returns_result(client, httpx_mock, sample_search_result):
    httpx_mock.add_response(json=sample_search_result)
    result = client.search()
    assert len(result.resultats) == 1
    assert result.resultats[0].id == "048KLTP"
    assert result.has_more is False


def test_search_204_returns_empty_result(client, httpx_mock):
    httpx_mock.add_response(status_code=204)
    result = client.search()
    assert result.resultats == []
    assert result.has_more is False


def test_search_206_sets_has_more(client, httpx_mock, sample_search_result):
    httpx_mock.add_response(status_code=206, json=sample_search_result)
    result = client.search()
    assert result.has_more is True


def test_search_400_raises_bad_request(client, httpx_mock):
    httpx_mock.add_response(status_code=400, text="Bad request")
    with pytest.raises(BadRequestError) as exc_info:
        client.search()
    assert exc_info.value.status_code == 400


def test_search_500_raises_server_error(client, httpx_mock):
    httpx_mock.add_response(status_code=500)
    with pytest.raises(ServerError) as exc_info:
        client.search()
    assert exc_info.value.status_code == 500


def test_search_timeout_raises_france_travail_error(client, httpx_mock):
    httpx_mock.add_exception(httpx.ConnectTimeout("timeout"))
    with pytest.raises(FranceTravailError) as exc_info:
        client.search()
    assert "Timeout" in str(exc_info.value)


def test_search_network_error_raises_france_travail_error(client, httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    with pytest.raises(FranceTravailError) as exc_info:
        client.search()
    assert "réseau" in str(exc_info.value)


def test_search_params_sent_as_query(client, httpx_mock, sample_search_result):
    httpx_mock.add_response(json=sample_search_result)
    client.search(SearchParams(typeContrat="CDI", departement="75"))
    request = httpx_mock.get_requests()[0]
    assert request.url.params["typeContrat"] == "CDI"
    assert request.url.params["departement"] == "75"


def test_search_authorization_header_sent(client, httpx_mock, sample_search_result, token):
    httpx_mock.add_response(json=sample_search_result)
    client.search()
    request = httpx_mock.get_requests()[0]
    assert request.headers["Authorization"] == f"Bearer {token}"
