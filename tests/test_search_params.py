from france_travail import SearchParams


def test_range_serializes_to_api_key():
    d = SearchParams(range_="0-49").to_query_dict()
    assert d["range"] == "0-49"
    assert "range_" not in d


def test_bool_true_is_lowercase():
    d = SearchParams(accesTravailleurHandicape=True).to_query_dict()
    assert d["accesTravailleurHandicape"] == "true"


def test_bool_false_is_lowercase():
    d = SearchParams(tempsPlein=False).to_query_dict()
    assert d["tempsPlein"] == "false"


def test_none_values_excluded():
    d = SearchParams(typeContrat="CDI").to_query_dict()
    assert d == {"typeContrat": "CDI"}


def test_empty_params_returns_empty_dict():
    assert SearchParams().to_query_dict() == {}


def test_int_params_serialized_as_string():
    d = SearchParams(distance=10, publieeDepuis=7).to_query_dict()
    assert d["distance"] == "10"
    assert d["publieeDepuis"] == "7"
