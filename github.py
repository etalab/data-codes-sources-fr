import os
import requests
from collections import defaultdict

from models import Organization, Repository


class GitHubOrg(object):
    def __init__(self, organization, swh_exists, base_url):
        super(GitHubOrg, self).__init__()
        self.organization = organization
        self.swh_exists = swh_exists
        self.base_url = base_url

    def __repr__(self):
        return "GitHubOrg: " + self.organization

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

        base_url = self.url("orgs/" + self.organization + "/repos?per_page=100")
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

            repo["name"] = repository["name"]
            repo["organization_name"] = repository["owner"]["login"]
            repo["platform"] = "GitHub"
            repo["repository_url"] = repository["html_url"]
            repo["description"] = repository["description"]
            repo["is_fork"] = repository["fork"]
            repo["is_archived"] = repository["archived"]
            repo["creation_date"] = repository["created_at"]
            repo["last_update"] = repository["updated_at"]
            repo["last_modification"] = repository["pushed_at"]
            repo["homepage"] = repository["homepage"]
            repo["stars_count"] = repository["stargazers_count"]
            repo["forks_count"] = repository["forks_count"]
            try:
                repo["license"] = self.clean_license(repository["license"]["name"])
            except Exception:
                repo["license"] = None
            repo["open_issues_count"] = repository["open_issues"]
            repo["language"] = repository["language"]
            repo["topics"] = ",".join(repository["topics"])
            repo.update(self.swh_attributes(repo))

            for k, v in Repository(**repo).to_dict_list().items():
                repos[k].extend(v)

        return repos

    def swh_attributes(self, repo):
        swh_url = self.swh_exists.swh_url(repo["repository_url"])
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
        base_url = self.url("orgs/" + self.organization)

        response = requests.get(base_url, headers=self.github_headers())
        if response.status_code == 404:
            return {}
        response.raise_for_status()

        data = response.json()

        mapping = [
            ("login", "login"),
            ("description", "description"),
            ("name", "name"),
            ("organization_url", "html_url"),
            ("avatar_url", "avatar_url"),
            ("website", "blog"),
            ("location", "location"),
            ("email", "email"),
            ("is_verified", "is_verified"),
            ("repositories_count", "public_repos"),
            ("creation_date", "created_at"),
        ]
        current_dict = {}
        for key, json_key in mapping:
            try:
                current_dict[key] = self.clean_data(data[json_key], key)
            except KeyError:
                current_dict[key] = None
        current_dict["platform"] = "GitHub"

        return Organization(**current_dict)

    def clean_data(self, value, key):
        if key == "website":
            if value and not value.startswith("http"):
                return "http://" + value
        return value
