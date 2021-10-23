import json

import pandas as pd

IN_FOLDER = "data/repositories/csv/"
OUT_FILEPATH = "data/stats.json"

df = pd.read_csv(IN_FOLDER + "all.csv")

repos_cnt = len(df)
orgs_cnt = len(df.groupby("organization_name"))
avg_repos_cnt = df.groupby("organization_name").count()["name"].agg("mean").round(2)
median_repos_cnt = df.groupby("organization_name").count()["name"].agg("median").round(2)
swh_exists_count = len(df.loc[df["software_heritage_exists"].fillna(False)])

top_orgs_by_repos = (
    df[["platform", "organization_name"]]
    .groupby(["platform", "organization_name"])
    .size()
    .to_frame("count")
    .sort_values(by="count", ascending=False)
    .head(10)
    .reset_index()
    .to_dict(orient="records")
)

top_orgs_by_stars = (
    df.groupby(["organization_name"])["stars_count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)

top_repos_stars = (
    df.groupby("repository_url")["stars_count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)
top_repos_forks = (
    df.groupby("repository_url")["forks_count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)
top_repos_issues = (
    df.groupby("repository_url")["open_issues_count"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .to_dict()
)

top_licenses = (
    df.fillna("Inconnue")
    .groupby("license")["name"]
    .count()
    .sort_values(ascending=False)
    .to_dict()
)

top_languages = (
    df.fillna("Inconnu")
    .groupby("language")["name"]
    .count()
    .sort_values(ascending=False)
    .head(11)
    .to_dict()
)

platforms = (
    df.groupby("platform")["name"].count().sort_values(ascending=False).to_dict()
)

res = {
    "repos_cnt": repos_cnt,
    "orgs_cnt": orgs_cnt,
    "avg_repos_cnt": avg_repos_cnt,
    "median_repos_cnt": median_repos_cnt,
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
        "ratio_in_archive": round(swh_exists_count / repos_cnt, 2),
    },
}

with open(OUT_FILEPATH, "w") as f:
    json.dump(res, f)
