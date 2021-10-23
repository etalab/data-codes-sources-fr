from collections import defaultdict

import requests

from models import Organization, Repository


class GitLabOrg(object):
    def __init__(self, organization, swh_exists, base_url):
        super(GitLabOrg, self).__init__()
        self.organization = organization
        self.swh_exists = swh_exists
        self.base_url = base_url

    def __repr__(self):
        return "GitLabOrg: " + self.organization

    def repos_for_org(self):
        def format_datetime(dt):
            # Remove milliseconds 2018-02-20T06:44:35.461Z
            return dt.split(".")[0] + "Z"

        data = []

        url = f"{self.base_url}groups/{self.organization}/projects?per_page=100&include_subgroups=true"
        response = requests.get(url)
        if response.status_code == 404:
            return {}
        response.raise_for_status()
        data.extend(response.json())

        repos = defaultdict(list)
        for repository in data:
            repo = {}

            repo["name"] = repository["path"]
            repo["organization_name"] = self.organization
            repo["platform"] = "GitLab"
            repo["repository_url"] = repository["web_url"]
            repo["description"] = repository["description"]
            repo["is_fork"] = None
            repo["is_archived"] = repository["archived"]
            repo["creation_date"] = format_datetime(repository["created_at"])
            repo["last_update"] = format_datetime(
                repository["last_activity_at"]
            )
            # derniere_modification really ought to be the equivalent of GitHub pushed_at but GitLab does not expose such information for now
            repo["last_modification"] = format_datetime(
                repository["last_activity_at"]
            )
            repo["homepage"] = None
            repo["stars_count"] = repository["star_count"]
            repo["forks_count"] = repository["forks_count"]
            repo["license"] = None
            try:
                repo["open_issues_count"] = repository["open_issues_count"]
            except KeyError:
                # Is it appropriate? Issues can be disabled, always leading to 0 issues
                repo["open_issues_count"] = 0
            repo["language"] = None
            repo["topics"] = ",".join(repository["tag_list"])
            repo.update(self.swh_attributes(repo))

            for k, v in Repository(**repo).to_dict_list().items():
                repos[k].extend(v)

        return repos

    def swh_attributes(self, repo):
        swh_url = self.swh_exists.swh_url(repo["repository_url"])
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

    def avatar_url(self, value):
        value = value or "nope"
        if value.startswith("http"):
            return value
        return None

    def get_org(self):
        url = self.base_url + "groups/" + self.organization

        response = requests.get(url)
        if response.status_code == 404:
            return {}
        response.raise_for_status()

        data = response.json()

        url_projects = self.base_url + "groups/" + self.organization + "/projects?include_subgroups=true"

        response_projects = requests.get(url_projects)
        if response_projects.status_code == 404:
            return {}
        response_projects.raise_for_status()

        data_projects = response_projects.json()

        res = {
            "login": data["path"],
            "description": data["description"],
            "name": data["name"],
            "organization_url": data["web_url"],
            "avatar_url": self.avatar_url(data["avatar_url"]),
            "website": None,
            "location": None,
            "email": None,
            "is_verified": None,
            "repos_cnt": len(data_projects),
            "creation_date": None,
            "platform": "GitLab",
        }

        return Organization(**res)
