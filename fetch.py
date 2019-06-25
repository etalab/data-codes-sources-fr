from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

from github import GitHubOrg
from gitlab import GitLabOrg
from storage import save_repos_for_org, save_org


def fetch_orgs():
    orgs = []

    resp = urlopen(
        "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/comptes-organismes-publics"
    )
    data = BytesIO(resp.read())

    for line in [l.decode("utf-8").strip() for l in data]:
        if line.startswith("https://github.com"):
            org_name = line.replace("https://github.com/", "").rstrip("/")
            orgs.append(GitHubOrg(org_name))
        if line.startswith("https://gitlab.com"):
            org_name = line.replace("https://gitlab.com/", "").rstrip("/")
            orgs.append(GitLabOrg(org_name))

    return orgs


organisations = fetch_orgs()

# Save details about each repo for an org
all_repos = defaultdict(list)
for organisation in organisations:
    print("Fetching repos for: ", organisation)

    repos = organisation.repos_for_org()

    for k, v in repos.items():
        all_repos[k].extend(v)

    save_repos_for_org(organisation, repos)

save_repos_for_org("all", all_repos)

# Save details about each org
all_orgs = defaultdict(list)
for organisation in organisations:
    data = organisation.get_org()

    if data == {}:
        continue
    print("Fetching details for: ", organisation)

    for k, v in data.to_dict().items():
        all_orgs[k].append(v)

    save_org(organisation, data.to_dict_list())

save_org("all", all_orgs)
