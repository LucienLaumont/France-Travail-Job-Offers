import pytest

from france_travail import find_secteur_by_rome, get_codes_rome, list_secteurs


def test_list_secteurs_count():
    assert len(list_secteurs()) == 89


def test_list_secteurs_structure():
    for s in list_secteurs():
        assert "id" in s and "libelle" in s


def test_get_codes_rome_returns_list():
    codes = get_codes_rome("1")
    assert len(codes) > 0
    assert all("code" in c and "libelle" in c for c in codes)


def test_get_codes_rome_invalid_raises_key_error():
    with pytest.raises(KeyError):
        get_codes_rome("999")


def test_find_secteur_by_rome_known_code():
    result = find_secteur_by_rome("M1805")
    assert any(s["id"] == "62" for s in result)


def test_find_secteur_by_rome_unknown_code_returns_empty():
    assert find_secteur_by_rome("ZZZZZZ") == []
