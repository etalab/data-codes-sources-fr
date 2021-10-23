from dataclasses import dataclass
from dataclasses import asdict as dataclasses_dict


class BaseModel(object):
    def to_dict(self):
        return dataclasses_dict(self)

    def to_dict_list(self):
        return {k: [v] for k, v in self.to_dict().items()}


@dataclass(frozen=True)
class Repository(BaseModel):
    name: str
    organization_nom: str
    platform: str
    repository_url: str
    description: str
    is_fork: bool
    is_archived: bool
    creation_date: str
    last_update: str
    last_modification: str
    homepage: str
    stars_count: int
    forks_count: int
    license: str
    open_issues_count: int
    language: str
    topics: str
    software_heritage_exists: bool
    software_heritage_url: str


@dataclass(frozen=True)
class Organization(BaseModel):
    login: str
    description: str
    name: str
    organization_url: str
    avatar_url: str
    website: str
    location: str
    email: str
    is_verified: bool
    repositories_count: int
    creation_date: str
    platform: str


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
