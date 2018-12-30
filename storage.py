import csv
import json

ORGS_FOLDER = 'data/organisations/'
REPOS_FOLDER = 'data/repertoires/'


def filename(organisation, mode, extension):
    if mode == 'repo':
        folder = REPOS_FOLDER
    elif mode == 'org':
        folder = ORGS_FOLDER
    else:
        raise ValueError
    if extension not in ['csv', 'json']:
        raise ValueError

    return '{folder}{extension}/{organisation}.{extension}'.format(
        folder=folder,
        extension=extension,
        organisation=organisation
    )


def save_data(organisation, data, mode):
    # Save in CSV
    with open(filename(organisation, mode, 'csv'), 'w') as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerows(zip(*data.values()))

    # Save in JSON
    with open(filename(organisation, mode, 'json'), 'w') as f:
        data = [dict(zip(data.keys(), i)) for i in zip(*data.values())]
        if len(data) == 1:
            data = data[0]
        json.dump(data, f, ensure_ascii=False)


def save_repos_for_org(organisation, data):
    save_data(organisation, data, 'repo')


def save_org(organisation, data):
    save_data(organisation, data, 'org')
