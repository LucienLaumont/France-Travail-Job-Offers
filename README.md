# france-travail-job-offers

SDK Python pour l'[API Offres d'emploi France Travail](https://www.data.gouv.fr/dataservices/api-offres-demploi).

## Installation

```bash
pip install france-travail-job-offers
```

## Authentification

L'accès à l'API nécessite un **Identifiant client** et une **Clé secrète** obtenus depuis le portail développeur France Travail.

Le SDK gère automatiquement le flux OAuth2 Client Credentials et le renouvellement des tokens.

- **Token URL** : `https://entreprise.francetravail.fr/connexion/oauth2/access_token?realm=/partenaire`
- **Scopes requis** : `o2dsoffre`, `api_offresdemploiv2`

## Usage rapide

```python
from france_travail import FranceTravailClient, SearchParams

with FranceTravailClient(client_id="...", client_secret="...") as client:
    result = client.search(SearchParams(
        motsCles="développeur",
        typeContrat="CDI",
        departement="75",
    ))

    print(f"{len(result.resultats)} offres trouvées")
    for offre in result.resultats:
        print(offre.intitule, "-", offre.lieuTravail.libelle if offre.lieuTravail else "")
```

## Limites

- **10 requêtes par seconde** maximum. Le SDK applique un rate limiter automatique.
- La pagination est limitée à 150 résultats par page, et l'index de départ ne peut pas dépasser 3000.

## Paramètres de recherche (`SearchParams`)

Tous les paramètres sont optionnels.

| Paramètre | Type | Description |
|---|---|---|
| `accesTravailleurHandicape` | `bool` | Offres ouvertes aux bénéficiaires de l'obligation d'emploi |
| `appellation` | `str` | Code appellation ROME (ex: `38444`) |
| `codeNAF` | `str` | Code NAF/APE, format `99.99X`, jusqu'à 200 valeurs séparées par virgule |
| `codeROME` | `str` | Code ROME, jusqu'à 200 valeurs séparées par virgule (ex: `D1102,D1104`) |
| `commune` | `str` | Code INSEE commune, jusqu'à 5 valeurs séparées par virgule |
| `departement` | `str` | Département, jusqu'à 5 valeurs séparées par virgule (ex: `33,31`) |
| `distance` | `int` | Rayon kilométrique autour de la commune |
| `domaine` | `str` | Domaine de l'offre (ex: `G17`) |
| `dureeContratMax` | `str` | Durée de contrat maximale en mois (ex: `24`) |
| `dureeContratMin` | `str` | Durée de contrat minimale en mois (ex: `0.5`) |
| `dureeHebdo` | `str` | Type de durée : `0` non précisé, `1` temps plein, `2` temps partiel |
| `dureeHebdoMax` | `str` | Durée maximale format HHMM (ex: `2430`) |
| `dureeHebdoMin` | `str` | Durée minimale format HHMM (ex: `800`) |
| `employeursHandiEngages` | `bool` | Employeurs engagés pour le handicap |
| `entreprisesAdaptees` | `bool` | Entreprises adaptées au handicap |
| `experience` | `str` | `0` non précisé, `1` < 1 an, `2` 1-3 ans, `3` > 3 ans |
| `experienceExigence` | `str` | `D` débutant, `S` souhaitée, `E` exigée |
| `grandDomaine` | `str` | Code grand domaine (ex: `M18` pour Informatique/Télécommunication) |
| `inclureLimitrophes` | `bool` | Inclure les départements limitrophes |
| `maxCreationDate` | `str` | Date max de création, format `yyyy-MM-dd'T'hh:mm:ss'Z'` |
| `minCreationDate` | `str` | Date min de création, format `yyyy-MM-dd'T'hh:mm:ss'Z'` |
| `modeSelectionPartenaires` | `str` | `INCLUS` ou `EXCLU` |
| `motsCles` | `str` | Mots-clés séparés par virgule (min 2 caractères chacun) |
| `natureContrat` | `str` | Code nature de contrat (ex: `E1`) |
| `niveauFormation` | `str` | Niveau de formation (ex: `NV3`) |
| `offresMRS` | `bool` | Offres avec méthode de recrutement par simulation uniquement |
| `offresManqueCandidats` | `bool` | Offres difficiles à pourvoir uniquement |
| `origineOffre` | `int` | `1` France Travail, `2` Partenaire |
| `partenaires` | `str` | Codes partenaires |
| `paysContinent` | `str` | Code pays ou continent (ex: `99127`) |
| `periodeSalaire` | `str` | `M` mensuel, `A` annuel, `H` horaire, `C` cachet |
| `permis` | `str` | Permis demandé (ex: `B`) |
| `publieeDepuis` | `int` | Offres publiées depuis maximum X jours (ex: `7`) |
| `qualification` | `str` | `0` non-cadre, `9` cadre |
| `range` | `str` | Pagination format `p-d` (ex: `0-49`), max 150 résultats, index max 3000 |
| `region` | `str` | Code région (ex: `75`) |
| `salaireMin` | `str` | Salaire minimum (requiert `periodeSalaire`) |
| `secteurActivite` | `str` | Division NAF (2 premiers chiffres), jusqu'à 2 valeurs (ex: `01,02`) |
| `sort` | `str` | `0` pertinence, `1` date décroissante, `2` distance croissante |
| `tempsPlein` | `bool` | Temps plein uniquement |
| `theme` | `str` | Thème ROME (ex: `12`) |
| `typeContrat` | `str` | Code type de contrat (ex: `CDI`, `CDD`) |

## Codes de réponse

| Code | Signification |
|---|---|
| `200` | Tous les résultats récupérés (`result.has_more = False`) |
| `204` | Aucune offre correspondante (liste vide retournée) |
| `206` | Résultats partiels, d'autres sont disponibles (`result.has_more = True`) |
| `400` | Mauvaise requête → `BadRequestError` |
| `500` | Erreur interne serveur → `ServerError` |

## Modèle de réponse

### `SearchResult`

| Champ | Type | Description |
|---|---|---|
| `resultats` | `list[Offre]` | Liste des offres retournées |
| `filtresPossibles` | `list[FiltrePossible]` | Filtres supplémentaires disponibles |
| `has_more` | `bool` | `True` si d'autres résultats sont disponibles (réponse 206) |

### `Offre` (champs principaux)

| Champ | Type | Description |
|---|---|---|
| `id` | `str` | Identifiant de l'offre (ex: `048KLTP`) |
| `intitule` | `str` | Intitulé du poste |
| `description` | `str` | Description de l'offre |
| `dateCreation` | `str` | Date de création (ISO 8601) |
| `dateActualisation` | `str` | Date de dernière actualisation (ISO 8601) |
| `lieuTravail` | `LieuTravail` | Lieu de travail (libellé, lat/lng, code postal, commune) |
| `romeCode` | `str` | Code ROME |
| `romeLibelle` | `str` | Libellé ROME |
| `entreprise` | `Entreprise` | Informations sur l'entreprise |
| `typeContrat` | `str` | Code type de contrat (`CDI`, `CDD`, etc.) |
| `typeContratLibelle` | `str` | Libellé du type de contrat |
| `experienceExige` | `str` | `D` débutant, `E` exigée, `S` souhaitée |
| `formations` | `list[Formation]` | Formations demandées |
| `competences` | `list[Competence]` | Compétences demandées |
| `salaire` | `Salaire` | Informations salariales |
| `contact` | `Contact` | Contact recruteur |
| `nombrePostes` | `int` | Nombre de postes disponibles |
| `accessibleTH` | `bool` | Accessible aux travailleurs handicapés |
| `alternance` | `bool` | Offre d'alternance |
| `offresManqueCandidats` | `bool` | Offre difficile à pourvoir |

## Gestion des erreurs

```python
from france_travail import (
    FranceTravailClient,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    ServerError,
    FranceTravailError,
)

try:
    result = client.search(params)
except AuthenticationError:
    print("Identifiants invalides ou token expiré")
except BadRequestError as e:
    print(f"Paramètres incorrects : {e}")
except RateLimitError:
    print("Limite de 10 req/s dépassée")
except ServerError:
    print("Erreur serveur France Travail")
except FranceTravailError as e:
    print(f"Erreur inattendue (HTTP {e.status_code}) : {e}")
```
