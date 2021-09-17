from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

from platforms import Detector as PlatformDetector
from storage import save_repos, save_orgs, save_packages


def fetch_orgs(detector):
    organisations = []

    # resp = urlopen(
    #     "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/comptes-organismes-publics"
    # )

    # data = BytesIO(resp.read())
    # data = set([l.lower().decode("utf-8").strip() for l in data])
    data = [
        "https://git.unicaen.fr/pdn-certic",
        "https://github.com/1024pix",
        "https://github.com/139bercy",
        "https://github.com/ansforge",
    ]
    
    data = set([l.lower().strip() for l in data])

    for line in data:
        try:
            organisations.extend(detector.to_orgs(line))
        except Exception as e:
            print(e)
    print(organisations)
    return organisations
    



detector = PlatformDetector()
organisations = fetch_orgs(detector)

# Save details about each repo for an org
all_repos = defaultdict(list)
for organisation in organisations:
    print("Fetching repos for: ", organisation)

    repos = organisation.repos_for_org()

    for k, v in repos.items():
        all_repos[k].extend(v)

save_repos(all_repos)

# Save packages created by each org
all_packs = all_repos

save_packages(all_repos)

# Save details about each org
all_orgs = defaultdict(list)
for organisation in organisations:
    data = organisation.get_org()

    if data == {}:
        continue
    print("Fetching details for: ", organisation)

    for k, v in data.to_dict().items():
        all_orgs[k].append(v)

save_orgs(all_orgs)
detector.save_swh_data()
