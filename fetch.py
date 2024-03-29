from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

from platforms import Detector as PlatformDetector
from storage import save_repos, save_orgs, save_libraries
from utils import fetch_libraries

def fetch_orgs(detector):
    organizations = []

    resp = urlopen(
        "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/comptes-organismes-publics"
    )
    data = BytesIO(resp.read())
    data = set([l.lower().decode("utf-8").strip() for l in data])

    for line in data:
        try:
            organizations.extend(detector.to_orgs(line))
        except Exception as e:
            print(e)

    return organizations


detector = PlatformDetector()
organizations = fetch_orgs(detector)

# Save details about each repo for an org
all_repos = defaultdict(list)
for organization in organizations:
    print("Fetching repos for: ", organization)

    repos = organization.repos_for_org()

    for k, v in repos.items():
        all_repos[k].extend(v)

save_repos(all_repos)

# Save details about each org
all_orgs = defaultdict(list)
for organization in organizations:
    data = organization.get_org()

    if data == {}:
        continue
    print("Fetching details for: ", organization)

    for k, v in data.to_dict().items():
        all_orgs[k].append(v)

save_orgs(all_orgs)

# Save libraries created by each org
all_packs = []

print("Fetching libraries from librairies.io")
libraries = fetch_libraries(all_orgs)

save_libraries(libraries)

detector.save_swh_data()
