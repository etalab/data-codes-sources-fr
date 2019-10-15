import os
import requests
from collections import defaultdict

from models import Organisation, Repository


class GitHubOrg(object):
    def __init__(self, organisation, swh_exists, base_url):
        super(GitHubOrg, self).__init__()
        self.organisation = organisation
        self.swh_exists = swh_exists
        self.base_url = base_url

    def __repr__(self):
        return "GitHubOrg: " + self.organisation

    def github_headers(self):
        return {
            "Authorization": "token " + os.getenv("GITHUB_TOKEN"),
            "Accept": ";".join(
                [
                    "application/vnd.github.v3+json",
                    "application/vnd.github.mercy-preview+json",
                ]
            ),
            "User-Agent": "Etalab. Contact: opensource@etalab.gouv.fr",
        }

    def url(self, path):
        return self.base_url + path

    def clean_license(self, value):
        if value == "Do What The F*ck You Want To Public License":
            return "Do What The Fuck You Want To Public License"
        return value

    def repos_for_org(self):
        data = []

        base_url = self.url("orgs/" + self.organisation + "/repos?per_page=100")
        response = requests.get(base_url, headers=self.github_headers())
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        data.extend(response.json())

        while "next" in response.links:
            url = response.links["next"]["url"]
            response = requests.get(url, headers=self.github_headers())
            data.extend(response.json())

        repos = defaultdict(list)
        for repository in data:
            repo = {}

            repo["nom"] = repository["name"]
            repo["organisation_nom"] = repository["owner"]["login"]
            repo["plateforme"] = "GitHub"
            repo["repertoire_url"] = repository["html_url"]
            repo["description"] = repository["description"]
            repo["est_fork"] = repository["fork"]
            repo["est_archive"] = repository["archived"]
            repo["date_creation"] = repository["created_at"]
            repo["derniere_mise_a_jour"] = repository["updated_at"]
            repo["derniere_modification"] = repository["pushed_at"]
            repo["page_accueil"] = repository["homepage"]
            repo["nombre_stars"] = repository["stargazers_count"]
            repo["nombre_forks"] = repository["forks_count"]
            try:
                repo["licence"] = self.clean_license(repository["license"]["name"])
            except Exception:
                repo["licence"] = None
            repo["nombre_issues_ouvertes"] = repository["open_issues"]
            repo["langage"] = repository["language"]
            repo["topics"] = ",".join(repository["topics"])
            repo.update(self.swh_attributes(repo))

            for k, v in Repository(**repo).to_dict_list().items():
                repos[k].extend(v)

        return repos

    def swh_attributes(self, repo):
        swh_url = self.swh_exists.swh_url(repo["repertoire_url"])
        res = {}

        if swh_url is False:
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
        base_url = self.url("orgs/" + self.organisation)

        response = requests.get(base_url, headers=self.github_headers())
        if response.status_code == 404:
            return {}
        response.raise_for_status()

        data = response.json()

        mapping = [
            ("login", "login"),
            ("description", "description"),
            ("nom", "name"),
            ("organisation_url", "html_url"),
            ("avatar_url", "avatar_url"),
            ("site_web", "blog"),
            ("adresse", "location"),
            ("email", "email"),
            ("est_verifiee", "is_verified"),
            ("nombre_repertoires", "public_repos"),
            ("date_creation", "created_at"),
        ]
        current_dict = {}
        for key, json_key in mapping:
            try:
                current_dict[key] = self.clean_data(data[json_key], key)
            except KeyError:
                current_dict[key] = None
        current_dict["plateforme"] = "GitHub"

        return Organisation(**current_dict)

    def clean_data(self, value, key):
        if key == "site_web":
            if value and not value.startswith("http"):
                return "http://" + value
        return value
