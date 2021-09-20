from dataclasses import dataclass
from dataclasses import asdict as dataclasses_dict


class BaseModel(object):
    def to_dict(self):
        return dataclasses_dict(self)

    def to_dict_list(self):
        return {k: [v] for k, v in self.to_dict().items()}


@dataclass(frozen=True)
class Repository(BaseModel):
    nom: str
    organisation_nom: str
    plateforme: str
    repertoire_url: str
    description: str
    est_fork: bool
    est_archive: bool
    date_creation: str
    derniere_mise_a_jour: str
    derniere_modification: str
    page_accueil: str
    nombre_stars: int
    nombre_forks: int
    licence: str
    nombre_issues_ouvertes: int
    langage: str
    topics: str
    software_heritage_exists: bool
    software_heritage_url: str


@dataclass(frozen=True)
class Organisation(BaseModel):
    login: str
    description: str
    nom: str
    organisation_url: str
    avatar_url: str
    site_web: str
    adresse: str
    email: str
    est_verifiee: bool
    nombre_repertoires: int
    date_creation: str
    plateforme: str

@dataclass(frozen=True)
class Package(BaseModel):
    deprecation_reason: bool
    description: str
    forks: int
    homepage: str
    keywords: str
    language: str
    latest_download_url: str
    latest_stable_release_number: str
    latest_stable_release_published_at: str
    license_normalized: bool
    licenses: str
    name: str
    normalized_licenses: str
    package_manager_url: str
    platform: str
    rank: int
    repository_url: str
    stars: int
    status:str