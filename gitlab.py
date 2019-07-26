import requests

from models import Organisation


class GitLabOrg(object):
    GITLAB_API_ROOT = "https://gitlab.com/api/v4/"

    def __init__(self, organisation):
        super(GitLabOrg, self).__init__()
        self.organisation = organisation

    def __repr__(self):
        return "GitLabOrg: " + self.organisation

    def repos_for_org(self):
        return {}

    def get_org(self):
        url = self.GITLAB_API_ROOT + "groups/" + self.organisation

        response = requests.get(url)
        if response.status_code == 404:
            return {}
        response.raise_for_status()

        data = response.json()

        res = {
            "login": data["path"],
            "description": data["description"],
            "nom": data["name"],
            "organisation_url": data["web_url"],
            "avatar_url": data["avatar_url"],
            "site_web": None,
            "adresse": None,
            "email": None,
            "est_verifiee": None,
            "nombre_repertoires": len(data["projects"]),
            "date_creation": None,
            "plateforme": "GitLab",
        }

        return Organisation(**res)
