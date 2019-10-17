import csv
import re

import requests

from swh import SwhExists
from github import GitHubOrg
from gitlab import GitLabOrg


class Detector(object):
    SUPPORTED_PLATFORMS = ["github", "gitlab"]
    SUPPORTED_BARE_PLATFORMS = ["gitlab"]

    def __init__(self):
        super(Detector, self).__init__()
        self.data = {}
        self.load_data()
        self.swh = SwhExists()

    def load_data(self):
        with open("platforms.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data[row["domain_name"]] = row["platform"]

    def save_swh_data(self):
        self.swh.save_data()

    def find_domain(self, url):
        for domain in self.data:
            if domain in url:
                return domain
        raise ValueError(f"Can't find a platform for {url}")

    def find_platform(self, url):
        domain = self.find_domain(url)
        if self.data[domain] in self.SUPPORTED_PLATFORMS:
            return self.data[domain]
        raise NotImplementedError(f"Platform for {url} is not supported")

    def platform_base_url(self, url):
        domain = self.find_domain(url)
        platform = self.data[domain]
        if platform == "github":
            return "https://api.github.com/"
        elif platform == "gitlab":
            return f"https://{domain}/api/v4/"
        else:
            raise NotImplementedError(f"Cannot find a base URL for {domain}")

    def is_bare_platform(self, url):
        for domain in self.data:
            platform = self.data[domain]
            if platform not in self.SUPPORTED_BARE_PLATFORMS:
                continue
            escaped_domain = domain.replace(".", "\.")
            if re.findall(f"{escaped_domain}$", url.rstrip("/")):
                return True
        return False

    def find_orgs(self, url):
        assert self.is_bare_platform(url)
        res = []
        should_continue = True
        url = f"{self.platform_base_url(url)}groups?per_page=100"

        while should_continue:
            response = requests.get(url)
            response.raise_for_status()
            for item in response.json():
                res.extend([org for org in self.to_orgs(item["web_url"])])
            should_continue = "next" in response.links
            if should_continue:
                url = response.links["next"]["url"]

        return res

    def to_orgs(self, url):
        if self.is_bare_platform(url):
            return self.find_orgs(url)
        platform = self.find_platform(url)
        org_name = url.rstrip("/").split("/")[-1]
        base_url = self.platform_base_url(url)
        if platform == "github":
            return [GitHubOrg(org_name, self.swh, base_url)]
        elif platform == "gitlab":
            return [GitLabOrg(org_name, self.swh, base_url)]
        else:
            raise NotImplementedError(f"Can't create class for {url}")
