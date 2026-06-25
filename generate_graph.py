import requests
import os

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

TOKEN = os.environ["GH_TOKEN"]
USERNAME = os.environ["USERNAME"]

headers = {
    "Authorization": f"token {TOKEN}"
}

repos = []

page = 1

while True:
    r = requests.get(
        f"https://api.github.com/user/repos?per_page=100&page={page}",
        headers=headers
    )

    data = r.json()

    if not data:
        break

    repos.extend(data)

    page += 1

totals = {}

for repo in repos:

    lang_url = repo["languages_url"]

    r = requests.get(
        lang_url,
        headers=headers
    )

    langs = r.json()

    for lang, size in langs.items():

        totals[lang] = totals.get(lang, 0) + size

total = sum(totals.values())

labels = []
sizes = []

for lang, value in sorted(
    totals.items(),
    key=lambda x: x[1],
    reverse=True
):

    labels.append(lang)

    sizes.append(
        value / total * 100
    )

plt.figure(figsize=(8,8))

plt.pie(
    sizes,
    labels=labels,
    autopct='%1.1f%%'
)

plt.title(
    "Programming Languages"
)

os.makedirs(
    "assets",
    exist_ok=True
)

plt.savefig(
    "assets/languages.svg",
    format="svg"
)
