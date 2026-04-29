from dataclasses import dataclass, field


@dataclass
class SearchParams:
    accesTravailleurHandicape: bool | None = None
    appellation: str | None = None
    codeNAF: str | None = None
    codeROME: str | None = None
    commune: str | None = None
    departement: str | None = None
    distance: int | None = None
    domaine: str | None = None
    dureeContratMax: str | None = None
    dureeContratMin: str | None = None
    dureeHebdo: str | None = None
    dureeHebdoMax: str | None = None
    dureeHebdoMin: str | None = None
    employeursHandiEngages: bool | None = None
    entreprisesAdaptees: bool | None = None
    experience: str | None = None
    experienceExigence: str | None = None
    grandDomaine: str | None = None
    inclureLimitrophes: bool | None = None
    maxCreationDate: str | None = None
    minCreationDate: str | None = None
    modeSelectionPartenaires: str | None = None
    motsCles: str | None = None
    natureContrat: str | None = None
    niveauFormation: str | None = None
    offresMRS: bool | None = None
    offresManqueCandidats: bool | None = None
    origineOffre: int | None = None
    partenaires: str | None = None
    paysContinent: str | None = None
    periodeSalaire: str | None = None
    permis: str | None = None
    publieeDepuis: int | None = None
    qualification: str | None = None
    range: str | None = None
    region: str | None = None
    salaireMin: str | None = None
    secteurActivite: str | None = None
    sort: str | None = None
    tempsPlein: bool | None = None
    theme: str | None = None
    typeContrat: str | None = None

    def to_query_dict(self) -> dict[str, str]:
        params: dict[str, str] = {}
        for key, value in self.__dict__.items():
            if value is None:
                continue
            if isinstance(value, bool):
                params[key] = "true" if value else "false"
            else:
                params[key] = str(value)
        return params
