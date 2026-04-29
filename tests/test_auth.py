import httpx
import pytest

from france_travail import AuthenticationError, FranceTravailClient


def _fresh_client() -> FranceTravailClient:
    return FranceTravailClient("test-client-id", "test-secret")


def test_token_fetched_on_first_call(httpx_mock, token, token_response):
    httpx_mock.add_response(method="POST", json=token_response)
    client = _fresh_client()
    assert client._auth.get_token() == token


def test_token_is_cached(httpx_mock, token_response):
    httpx_mock.add_response(method="POST", json=token_response)
    client = _fresh_client()
    client._auth.get_token()
    client._auth.get_token()
    assert len(httpx_mock.get_requests()) == 1


def test_token_refreshed_on_expiry(httpx_mock, token_response):
    httpx_mock.add_response(method="POST", json=token_response)
    httpx_mock.add_response(method="POST", json={**token_response, "access_token": "new-token"})
    client = _fresh_client()
    client._auth.get_token()
    client._auth._expires_at = 0.0
    assert client._auth.get_token() == "new-token"


def test_auth_raises_on_401(httpx_mock):
    httpx_mock.add_response(method="POST", status_code=401, text="Unauthorized")
    client = _fresh_client()
    with pytest.raises(AuthenticationError) as exc_info:
        client._auth.get_token()
    assert exc_info.value.status_code == 401


def test_auth_raises_on_network_error(httpx_mock):
    httpx_mock.add_exception(httpx.ConnectError("connection refused"))
    client = _fresh_client()
    with pytest.raises(AuthenticationError):
        client._auth.get_token()
