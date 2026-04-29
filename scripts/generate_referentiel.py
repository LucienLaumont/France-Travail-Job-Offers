"""
Re-génère france_travail/data/secteurs_naf_rome.json depuis le fichier xlsx dans docs/.
À relancer après chaque mise à jour du fichier source.

Usage :
    pip install openpyxl
    python scripts/generate_referentiel.py
"""

import json
from pathlib import Path

import openpyxl

DOCS_DIR = Path(__file__).parent.parent / "docs"
OUTPUT = Path(__file__).parent.parent / "france_travail" / "data" / "secteurs_naf_rome.json"


def find_xlsx() -> Path:
    files = list(DOCS_DIR.glob("*.xlsx"))
    if not files:
        raise FileNotFoundError(f"Aucun fichier .xlsx trouvé dans {DOCS_DIR}")
    if len(files) > 1:
        print(f"Plusieurs fichiers trouvés, utilisation de : {files[0].name}")
    return files[0]


def parse(path: Path) -> dict:
    wb = openpyxl.load_workbook(path, read_only=True)
    ws = wb["Secteur NAF 09-2025"]
    secteurs: dict = {}
    current_id = None
    for col1, col2 in ws.iter_rows(values_only=True):
        if not col1:
            continue
        try:
            int(str(col1))
            current_id = str(col1)
            secteurs[current_id] = {"libelle": col2, "codes_rome": []}
        except ValueError:
            if current_id is not None:
                secteurs[current_id]["codes_rome"].append({"code": col1, "libelle": col2})
    return secteurs


def main() -> None:
    xlsx = find_xlsx()
    print(f"Lecture de : {xlsx.name}")
    secteurs = parse(xlsx)
    nb_rome = sum(len(s["codes_rome"]) for s in secteurs.values())
    OUTPUT.write_text(json.dumps(secteurs, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Généré : {OUTPUT} ({len(secteurs)} secteurs, {nb_rome} codes ROME)")


if __name__ == "__main__":
    main()
