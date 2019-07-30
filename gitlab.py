from collections import defaultdict

import requests

from models import Organisation, Repository


class GitLabOrg(object):
    GITLAB_API_ROOT = "https://gitlab.com/api/v4/"

    def __init__(self, organisation):
        super(GitLabOrg, self).__init__()
        self.organisation = organisation

    def __repr__(self):
        return "GitLabOrg: " + self.organisation

    def repos_for_org(self):
        def format_datetime(dt):
            # Remove milliseconds 2018-02-20T06:44:35.461Z
            return dt.split(".")[0] + "Z"

        data = []

        url = f"{self.GITLAB_API_ROOT}groups/{self.organisation}/projects"
        response = requests.get(url)
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        data.extend(response.json())

        repos = defaultdict(list)
        for repository in data:
            repo = {}

            repo["nom"] = repository["path"]
            repo["organisation_nom"] = self.organisation
            repo["plateforme"] = "GitLab"
            repo["repertoire_url"] = repository["web_url"]
            repo["description"] = repository["description"]
            repo["est_fork"] = None
            repo["date_creation"] = format_datetime(repository["created_at"])
            repo["derniere_mise_a_jour"] = format_datetime(
                repository["last_activity_at"]
            )
            repo["page_accueil"] = None
            repo["nombre_stars"] = repository["star_count"]
            repo["nombre_forks"] = repository["forks_count"]
            repo["licence"] = None
            try:
                repo["nombre_issues_ouvertes"] = repository["open_issues_count"]
            except KeyError:
                # Is it appropriate? Issues can be disabled, always leading to 0 issues
                repo["nombre_issues_ouvertes"] = 0
            repo["langage"] = None
            repo["topics"] = ",".join(repository["tag_list"])

            for k, v in Repository(**repo).to_dict_list().items():
                repos[k].extend(v)

        return repos

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
