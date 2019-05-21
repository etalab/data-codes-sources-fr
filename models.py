from dataclasses import dataclass
from dataclasses import asdict as dataclasses_dict


@dataclass(frozen=True)
class Organisation:
    login: str
    description: str
    nom: str
    organisation_url: str
    site_web: str
    adresse: str
    email: str
    est_verifiee: bool
    nombre_repertoires: int
    date_creation: str
    plateforme: str

    def to_dict(self):
        return dataclasses_dict(self)

    def to_dict_list(self):
        return {k: [v] for k, v in self.to_dict().items()}
