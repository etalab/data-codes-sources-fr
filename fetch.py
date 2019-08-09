from collections import defaultdict
from io import BytesIO
from urllib.request import urlopen

from platforms import Detector as PlatformDetector
from storage import save_repos_for_org, save_org


def fetch_orgs(detector):
    organisations = []

    resp = urlopen(
        "https://raw.githubusercontent.com/DISIC/politique-de-contribution-open-source/master/comptes-organismes-publics"
    )
    data = BytesIO(resp.read())
    data = set([l.lower().decode("utf-8").strip() for l in data])

    for line in data:
        try:
            organisations.append(detector.to_org(line))
        except Exception as e:
            print(e)

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
detector.save_swh_data()
