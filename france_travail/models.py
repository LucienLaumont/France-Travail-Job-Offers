from pydantic import BaseModel


class LieuTravail(BaseModel):
    libelle: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    codePostal: str | None = None
    commune: str | None = None


class Entreprise(BaseModel):
    nom: str | None = None
    description: str | None = None
    logo: str | None = None
    url: str | None = None
    entrepriseAdaptee: bool | None = None


class Formation(BaseModel):
    codeFormation: str | None = None
    domaineLibelle: str | None = None
    niveauLibelle: str | None = None
    commentaire: str | None = None
    exigence: str | None = None


class Langue(BaseModel):
    libelle: str | None = None
    exigence: str | None = None


class Permis(BaseModel):
    libelle: str | None = None
    exigence: str | None = None


class Competence(BaseModel):
    code: str | None = None
    libelle: str | None = None
    exigence: str | None = None


class ComplementSalaire(BaseModel):
    code: str | None = None
    libelle: str | None = None


class Salaire(BaseModel):
    libelle: str | None = None
    commentaire: str | None = None
    complement1: str | None = None
    complement2: str | None = None
    listeComplements: list[ComplementSalaire] = []


class Contact(BaseModel):
    nom: str | None = None
    coordonnees1: str | None = None
    coordonnees2: str | None = None
    coordonnees3: str | None = None
    telephone: str | None = None
    courriel: str | None = None
    commentaire: str | None = None
    urlRecruteur: str | None = None
    urlPostulation: str | None = None


class Agence(BaseModel):
    telephone: str | None = None
    courriel: str | None = None


class QualiteProfessionnelle(BaseModel):
    libelle: str | None = None
    description: str | None = None


class OrigineOffre(BaseModel):
    origine: str | None = None
    urlOrigine: str | None = None
    partenaires: list[dict] = []


class ContexteTravail(BaseModel):
    horaires: list[str] = []
    conditionsExercice: list[str] = []


class FiltrePossible(BaseModel):
    filtre: str | None = None
    agregation: list[dict] = []


class Offre(BaseModel):
    id: str | None = None
    intitule: str | None = None
    description: str | None = None
    dateCreation: str | None = None
    dateActualisation: str | None = None
    lieuTravail: LieuTravail | None = None
    romeCode: str | None = None
    romeLibelle: str | None = None
    appellationlibelle: str | None = None
    entreprise: Entreprise | None = None
    typeContrat: str | None = None
    typeContratLibelle: str | None = None
    natureContrat: str | None = None
    experienceExige: str | None = None
    experienceLibelle: str | None = None
    experienceCommentaire: str | None = None
    formations: list[Formation] = []
    langues: list[Langue] = []
    permis: list[Permis] = []
    outilsBureautiques: list[str] = []
    competences: list[Competence] = []
    salaire: Salaire | None = None
    dureeTravailLibelle: str | None = None
    dureeTravailLibelleConverti: str | None = None
    complementExercice: str | None = None
    conditionExercice: str | None = None
    alternance: bool | None = None
    contact: Contact | None = None
    agence: Agence | None = None
    nombrePostes: int | None = None
    accessibleTH: bool | None = None
    deplacementCode: str | None = None
    deplacementLibelle: str | None = None
    qualificationCode: str | None = None
    qualificationLibelle: str | None = None
    codeNAF: str | None = None
    secteurActivite: str | None = None
    secteurActiviteLibelle: str | None = None
    qualitesProfessionnelles: list[QualiteProfessionnelle] = []
    trancheEffectifEtab: str | None = None
    origineOffre: OrigineOffre | None = None
    offresManqueCandidats: bool | None = None
    contexteTravail: ContexteTravail | None = None
    entrepriseAdaptee: bool | None = None
    employeurHandiEngage: bool | None = None


class SearchResult(BaseModel):
    resultats: list[Offre] = []
    filtresPossibles: list[FiltrePossible] = []
    has_more: bool = False
