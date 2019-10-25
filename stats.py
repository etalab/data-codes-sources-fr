import json

import pandas as pd

IN_FOLDER = "data/repertoires/csv/"
OUT_FILEPATH = "data/stats.json"

df = pd.read_csv(IN_FOLDER + "all.csv")

nb_repos = len(df)
nb_orgs = len(df.groupby("organisation_nom"))
avg_nb_repos = df.groupby("organisation_nom").count()["nom"].agg("mean").round(2)
median_nb_repos = df.groupby("organisation_nom").count()["nom"].agg("median").round(2)
swh_exists_count = len(df.loc[df["software_heritage_exists"].fillna(False)])

top_orgs_by_repos = (
    df[["plateforme", "organisation_nom"]]
    .groupby(["plateforme", "organisation_nom"])
    .size()
    .to_frame("count")
    .sort_values(by="count", ascending=False)
    .head(10)
    .reset_index()
    .to_dict(orient="records")
)

top_orgs_by_stars = (
    df.groupby(["organisation_nom"])["nombre_stars"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)

top_repos_stars = (
    df.groupby("repertoire_url")["nombre_stars"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)
top_repos_forks = (
    df.groupby("repertoire_url")["nombre_forks"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)
top_repos_issues = (
    df.groupby("repertoire_url")["nombre_issues_ouvertes"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)

top_licenses = (
    df.fillna("Inconnue")
    .groupby("licence")["nom"]
    .count()
    .sort_values(ascending=False)
    .to_dict()
)

top_languages = (
    df.fillna("Inconnu")
    .groupby("langage")["nom"]
    .count()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)

platforms = (
    df.groupby("plateforme")["nom"].count().sort_values(ascending=False).to_dict()
)

res = {
    "nb_repos": nb_repos,
    "nb_orgs": nb_orgs,
    "avg_nb_repos": avg_nb_repos,
    "median_nb_repos": median_nb_repos,
    "top_orgs_by_repos": top_orgs_by_repos,
    "top_orgs_by_stars": top_orgs_by_stars,
    "top_repos_stars": top_repos_stars,
    "top_repos_forks": top_repos_forks,
    "top_repos_issues": top_repos_issues,
    "top_licenses": top_licenses,
    "top_languages": top_languages,
    "platforms": platforms,
    "software_heritage": {
        "repos_in_archive": swh_exists_count,
        "ratio_in_archive": round(swh_exists_count / nb_repos, 2),
    },
}

with open(OUT_FILEPATH, "w") as f:
    json.dump(res, f)
