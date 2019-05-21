import os
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

from models import Organisation

GITHUB_API_ROOT = "https://api.github.com/"

retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])

requests.Session().mount("https://", HTTPAdapter(max_retries=retries))


def github_headers():
    return {
        "Authorization": "token " + os.getenv("GITHUB_TOKEN"),
        "Accept": ";".join(
            [
                "application/vnd.github.v3+json",
                "application/vnd.github.mercy-preview+json",
            ]
        ),
        "User-Agent": "AntoineAugusti",
    }


def repos_for_org(organisation):
    data = []

    base_url = GITHUB_API_ROOT + "orgs/" + organisation + "/repos?per_page=100"
    response = requests.get(base_url, headers=github_headers())
    if response.status_code == 404:
        return []
    response.raise_for_status()
    data.extend(response.json())

    while "next" in response.links:
        url = response.links["next"]["url"]
        response = requests.get(url, headers=github_headers())
        data.extend(response.json())

    return data


def clean_data(value, key):
    if key == "site_web":
        if value and not value.startswith("http"):
            return "http://" + value
    return value


def get_org(organisation):
    base_url = GITHUB_API_ROOT + "orgs/" + organisation

    response = requests.get(base_url, headers=github_headers())
    if response.status_code == 404:
        return None
    response.raise_for_status()

    data = response.json()

    mapping = [
        ("login", "login"),
        ("description", "description"),
        ("nom", "name"),
        ("organisation_url", "html_url"),
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
            current_dict[key] = clean_data(data[json_key], key)
        except KeyError:
            current_dict[key] = None
    current_dict["plateforme"] = "GitHub"

    return Organisation(**current_dict)
