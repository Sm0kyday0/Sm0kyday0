import os
import requests

TOKEN = os.environ["GH_TOKEN"]
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
    r = requests.get(
        repo["languages_url"],
        headers=headers
    )
    langs = r.json()
    for lang, size in langs.items():
        totals[lang] = totals.get(lang, 0) + size

langs = sorted(
    totals.items(),
    key=lambda x: x[1],
    reverse=True
)
top = langs[:5]
other = sum(
    value for _, value in langs[5:]
)
if other > 0:
    top.append(("Other", other))

total_size = sum(
    value for _, value in top
)

colors = {
    "Java": "#b07219",
    "Kotlin": "#A97BFF",
    "JavaScript": "#f1e05a",
    "TypeScript": "#3178c6",
    "Python": "#3572A5",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
    "C": "#555555",
    "C++": "#f34b7d",
    "C#": "#178600",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Go": "#00ADD8",
    "Rust": "#dea584",
    "Shell": "#89e051",
    "Lua": "#000080",
    "Swift": "#F05138",
    "Dart": "#00B4AB",
    "Vue": "#41B883",
    "Other": "#8b949e"
}

svg_width = 900
bar_width = 860
height = 120 + len(top) * 28
svg = []
svg.append(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{height}">'
)
svg.append(
    '<rect x="20" y="20" width="860" height="14" rx="7" ry="7" fill="#21262d"/>'
)

x = 20
for lang, value in top:
    percent = value / total_size * 100
    width = bar_width * percent / 100
    color = colors.get(lang, "#8b949e")
    svg.append(
        f'<rect x="{x}" y="20" width="{width}" height="14" fill="{color}"/>'
    )
    x += width

y = 65
for lang, value in top:
    percent = value / total_size * 100
    color = colors.get(lang, "#8b949e")
    svg.append(
        f'<circle cx="30" cy="{y-4}" r="6" fill="{color}"/>'
    )
    svg.append(
        f'<text '
        f'x="45" '
        f'y="{y}" '
        f'fill="#c9d1d9" '
        f'font-size="14" '
        f'font-family="Segoe UI">'
        f'{lang} {percent:.2f}%'
        f'</text>'
    )
    y += 28

svg.append("</svg>")

os.makedirs("assets", exist_ok=True)
with open(
    "assets/languages.svg",
    "w",
    encoding="utf-8"
) as f:
    f.write("\n".join(svg))
