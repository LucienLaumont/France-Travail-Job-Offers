import json
from pathlib import Path

_DATA_FILE = Path(__file__).parent / "data" / "secteurs_naf_rome.json"

_secteurs: dict | None = None


def _load() -> dict:
    global _secteurs
    if _secteurs is None:
        with open(_DATA_FILE, encoding="utf-8") as f:
            _secteurs = json.load(f)
    return _secteurs


def list_secteurs() -> list[dict]:
    """Retourne tous les secteurs NAF avec leur id et libellé."""
    return [
        {"id": sid, "libelle": data["libelle"]}
        for sid, data in _load().items()
    ]


def get_codes_rome(secteur_id: str) -> list[dict]:
    """Retourne les codes ROME associés à un secteur NAF (id sous forme de chaîne).

    Chaque élément est un dict {"code": str, "libelle": str}.
    Lève KeyError si le secteur n'existe pas.
    """
    secteurs = _load()
    if secteur_id not in secteurs:
        raise KeyError(f"Secteur NAF '{secteur_id}' introuvable. Utilisez list_secteurs() pour voir les ids valides.")
    return secteurs[secteur_id]["codes_rome"]


def find_secteur_by_rome(code_rome: str) -> list[dict]:
    """Retourne les secteurs NAF qui contiennent un code ROME donné.

    Chaque élément est un dict {"id": str, "libelle": str}.
    """
    return [
        {"id": sid, "libelle": data["libelle"]}
        for sid, data in _load().items()
        if any(entry["code"] == code_rome for entry in data["codes_rome"])
    ]
