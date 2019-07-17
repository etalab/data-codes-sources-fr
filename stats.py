import json

import pandas as pd

IN_FOLDER = "data/repertoires/csv/"
OUT_FILEPATH = "data/stats.json"

df = pd.read_csv(IN_FOLDER + "all.csv")

nb_repos = len(df)
nb_orgs = len(df.groupby("organisation_nom"))
avg_nb_repos = df.groupby("organisation_nom").count()["nom"].agg("mean")
median_nb_repos = df.groupby("organisation_nom").count()["nom"].agg("median")

top_orgs_by_repos = (
    df.groupby("organisation_nom")
    .count()["nom"]
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
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
}

with open(OUT_FILEPATH, "w") as f:
    json.dump(res, f)
