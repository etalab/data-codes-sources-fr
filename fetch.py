import yaml

from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

from github import repos_for_org, get_org
from storage import save_repos_for_org, save_org


def fetch_orgs():
    orgs = []

    resp = urlopen(
        "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/comptes-organismes-publics"
    )
    data = BytesIO(resp.read())
    for line in [l.decode("utf-8").strip() for l in data]:
        if line.startswith("https://github.com"):
            orgs.append(line.replace("https://github.com/", "").rstrip("/"))

    resp = urlopen(
        "https://raw.githubusercontent.com/github/government.github.com/gh-pages/_data/governments.yml"
    )
    french_orgs = yaml.safe_load(resp.read())["France"]
    orgs.extend(french_orgs)

    seen = set()
    unique_orgs = [x for x in orgs if x.lower() not in seen and not seen.add(x.lower())]
    unique_orgs.sort()

    return unique_orgs


organisations = fetch_orgs()

# Save details about each repo for an org
all_repos = defaultdict(list)
for organisation in organisations:
    print("Fetching repos for: ", organisation)

    repos = repos_for_org(organisation)

    for k, v in repos.items():
        all_repos[k].extend(v)

    save_repos_for_org(organisation, repos)

save_repos_for_org("all", all_repos)

# Save details about each org
all_orgs = defaultdict(list)
for organisation in organisations:
    data = get_org(organisation)

    if data == {}:
        continue
    print("Fetching details for: ", organisation)

    for k, v in data.to_dict().items():
        all_orgs[k].append(v)

    save_org(organisation, data.to_dict_list())

save_org("all", all_orgs)
