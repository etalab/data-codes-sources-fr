import os
import requests, json, time
from collections import defaultdict

from models import Library

def fetch_library(org):
    api_key = os.getenv("LIBRARIESIO_API_KEY")
    base_url = "https://libraries.io/api/github/"+ org +"/projects?api_key=" + api_key
    response = requests.get(base_url)
    if response.status_code == 404 or response.status_code == 500:
        return {}
    response.raise_for_status()

    data = response.json()

    mapping = [
        ("deprecation_reason", "deprecation_reason"),
        ("description", "description"),
        ("name", "name"),
        ("forks", "forks"),
        ("homepage", "homepage"),
        ("keywords", "keywords"),
        ("language", "language"),
        ("stars", "stars"),
        ("latest_download_url", "latest_download_url"),
        ("latest_stable_release_number", "latest_stable_release_number"),
        ("latest_stable_release_published_at", "latest_stable_release_published_at"),
        ("license_normalized", "license_normalized"),
        ("licenses", "licenses"),
        ("normalized_licenses", "normalized_licenses"),
        ("library_manager_url", "library_manager_url"),
        ("platform", "platform"),
        ("rank", "rank"),
        ("repository_url", "repository_url"),
        ("status", "status"),
    ]
    
    org_libraries = defaultdict(list)
    if len(data) > 0:
        for pack in data:
            current_dict = {}
            for key, json_key in mapping:
                try:
                    current_dict[key] = str(pack[json_key])
                except KeyError:
                    current_dict[key] = None
            p = Library(**current_dict)
            for k, v in p.to_dict().items():
                org_libraries[k].append(v)
    return org_libraries



def fetch_libraries(orgs):
    json_orgs = json.loads(json.dumps(orgs))
    all_packs = defaultdict(list)
    for k,v in enumerate(json_orgs["login"]):
        if json_orgs["plateforme"][k] == "GitHub":
            time.sleep(1)
            libraries = fetch_library(v)
            for key in libraries:
                all_packs[key].extend(libraries[key])
    return all_packs
