import csv
import json
import os
import requests
import yaml

from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

ORGS_FOLDER = 'data/organisations/'
REPOS_FOLDER = 'data/repertoires/'

GITHUB_API_ROOT = 'https://api.github.com/'


def fetch_orgs():
    orgs = []

    resp = urlopen("https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/OrgAccounts")
    data = BytesIO(resp.read())
    for line in [l.decode("utf-8").strip() for l in data]:
        if line.startswith('https://github.com'):
            orgs.append(line.replace('https://github.com/', '').rstrip('/'))

    resp = urlopen('https://raw.githubusercontent.com/github/government.github.com/gh-pages/_data/governments.yml')
    french_orgs = yaml.safe_load(resp.read())['France']
    orgs.extend(french_orgs)

    seen = set()
    unique_orgs = [x for x in orgs if x.lower() not in seen and not seen.add(x.lower())]
    unique_orgs.sort()

    return unique_orgs


def repos_for_org(organisation):
    data = []

    base_url = GITHUB_API_ROOT + 'orgs/' + organisation + '/repos?per_page=100'
    headers = {
        'Authorization': 'token ' + os.getenv('GITHUB_TOKEN'),
        'Accept': ';'.join([
            'application/vnd.github.v3+json',
            'application/vnd.github.mercy-preview+json'
        ]),
        'User-Agent': 'AntoineAugusti'
    }
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        return []
    data.extend(response.json())

    while 'next' in response.links:
        response = requests.get(response.links['next']['url'], headers=headers)
        data.extend(response.json())

    return data


def save_repos_for_org(organisation, data):
    def repo_filename(organisation, mode):
        if mode not in ['csv', 'json']:
            raise ValueError
        return '{folder}{mode}/{organisation}.{mode}'.format(
            folder=REPOS_FOLDER,
            mode=mode,
            organisation=organisation
        )
    # Save in CSV
    with open(repo_filename(organisation, 'csv'), 'w') as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerows(zip(*data.values()))

    # Save in JSON
    with open(repo_filename(organisation, 'json'), 'w') as f:
        data = [dict(zip(data.keys(), i)) for i in zip(*data.values())]
        json.dump(data, f, ensure_ascii=False)

all_repos = defaultdict(list)
for org in fetch_orgs():
    repos = defaultdict(list)
    print('Fetching: ', org)

    for repo in repos_for_org(org):
        repos['nom'].append(repo['name'])
        repos['organisation_nom'].append(repo['owner']['login'])
        repos['organisation_url'].append(repo['owner']['html_url'])
        repos['repertoire_url'].append(repo['html_url'])
        repos['description'].append(repo['description'])
        repos['est_fork'].append(repo['fork'])
        repos['date_creation'].append(repo['created_at'])
        repos['derniere_mise_a_jour'].append(repo['updated_at'])
        repos['homepage'].append(repo['homepage'])
        repos['nombre_stars'].append(repo['stargazers_count'])
        repos['nombre_forks'].append(repo['forks_count'])
        try:
            repos['licence'].append(repo['licence']['name'])
        except Exception as e:
            repos['licence'].append(None)
        repos['nombre_issues_ouvertes'].append(repo['open_issues'])
        repos['langage'].append(repo['language'])
        repos['topics'].append(','.join(repo['topics']))

    for k, v in repos.items():
        all_repos[k].extend(v)

    save_repos_for_org(org, repos)

save_repos_for_org('all', all_repos)
