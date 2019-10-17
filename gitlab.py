from collections import defaultdict

import requests

from models import Organisation, Repository


class GitLabOrg(object):
    def __init__(self, organisation, swh_exists, base_url):
        super(GitLabOrg, self).__init__()
        self.organisation = organisation
        self.swh_exists = swh_exists
        self.base_url = base_url

    def __repr__(self):
        return "GitLabOrg: " + self.organisation

    def repos_for_org(self):
        def format_datetime(dt):
            # Remove milliseconds 2018-02-20T06:44:35.461Z
            return dt.split(".")[0] + "Z"

        data = []

        url = f"{self.base_url}groups/{self.organisation}/projects?per_page=100"
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
            repo["est_archive"] = repository["archived"]
            repo["date_creation"] = format_datetime(repository["created_at"])
            repo["derniere_mise_a_jour"] = format_datetime(
                repository["last_activity_at"]
            )
            # derniere_modification really ought to be the equivalent of GitHub pushed_at but GitLab does not expose such information for now
            repo["derniere_modification"] = format_datetime(
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
            repo.update(self.swh_attributes(repo))

            for k, v in Repository(**repo).to_dict_list().items():
                repos[k].extend(v)

        return repos

    def swh_attributes(self, repo):
        swh_url = self.swh_exists.swh_url(repo["repertoire_url"])
        res = {}

        if not swh_url:
            res["software_heritage_exists"] = False
            res["software_heritage_url"] = None
        elif swh_url is None:
            res["software_heritage_exists"] = None
            res["software_heritage_url"] = None
        else:
            res["software_heritage_exists"] = True
            res["software_heritage_url"] = swh_url

        return res

    def get_org(self):
        url = self.base_url + "groups/" + self.organisation

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
