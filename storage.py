import csv
import json

ORGS_FOLDER = "data/organisations/"
REPOS_FOLDER = "data/repertoires/"


def filename(mode, extension):
    if mode == "repo":
        folder = REPOS_FOLDER
    elif mode == "org":
        folder = ORGS_FOLDER
    else:
        raise ValueError
    if extension not in ["csv", "json"]:
        raise ValueError

    return "{folder}{extension}/all.{extension}".format(
        folder=folder, extension=extension
    )


def save_data(data, mode):
    # Save in CSV
    with open(filename(mode, "csv"), "w") as f:
        w = csv.writer(f)
        w.writerow(data.keys())
        w.writerows(set(zip(*data.values())))

    # Save in JSON
    with open(filename(mode, "json"), "w") as f:
        data = [dict(zip(data.keys(), i)) for i in set(zip(*data.values()))]
        if mode == "org" and len(data) == 1:
            data = data[0]
        json.dump(data, f, ensure_ascii=False)


def save_repos(data):
    save_data(data, "repo")


def save_orgs(data):
    save_data(data, "org")
