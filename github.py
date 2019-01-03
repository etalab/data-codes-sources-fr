import os
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

GITHUB_API_ROOT = 'https://api.github.com/'

retries = Retry(
    total=5,
    backoff_factor=0.1,
    status_forcelist=[500, 502, 503, 504])

requests.Session().mount('https://', HTTPAdapter(max_retries=retries))


def github_headers():
    return {
        'Authorization': 'token ' + os.getenv('GITHUB_TOKEN'),
        'Accept': ';'.join([
            'application/vnd.github.v3+json',
            'application/vnd.github.mercy-preview+json'
        ]),
        'User-Agent': 'AntoineAugusti'
    }


def repos_for_org(organisation):
    data = []

    base_url = GITHUB_API_ROOT + 'orgs/' + organisation + '/repos?per_page=100'
    response = requests.get(base_url, headers=github_headers())
    if response.status_code == 404:
        return []
    response.raise_for_status()
    data.extend(response.json())

    while 'next' in response.links:
        url = response.links['next']['url']
        response = requests.get(url, headers=github_headers())
        data.extend(response.json())

    return data


def get_org(organisation):
    base_url = GITHUB_API_ROOT + 'orgs/' + organisation

    response = requests.get(base_url, headers=github_headers())
    if response.status_code == 404:
        return None
    response.raise_for_status()

    return response.json()
