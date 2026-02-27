from fastapi import FastAPI, Query
import requests
from itertools import combinations
from collections import defaultdict

app = FastAPI()

BASE_URL = "https://rickandmortyapi.com/api"


def safe_get(url, params=None):
    r = requests.get(url, params=params)
    if r.status_code == 404:
        return []
    r.raise_for_status()
    return r.json().get("results", [])


@app.get("/search")
def search(term: str = Query(...), limit: int | None = None):
    results = []

    for resource, rtype in [
        ("character", "character"),
        ("location", "location"),
        ("episode", "episode"),
    ]:
        items = safe_get(f"{BASE_URL}/{resource}", {"name": term})
        for i in items:
            results.append({
                "name": i["name"],
                "type": rtype,
                "url": i["url"],
            })

    if limit:
        results = results[:limit]

    return results


@app.get("/top-pairs")
def top_pairs(
    min: int = 0,
    max: int | None = None,
    limit: int = 20,
):
    pair_counts = defaultdict(int)
    character_cache = {}

    page = 1
    while True:
        r = requests.get(f"{BASE_URL}/episode", params={"page": page})
        if r.status_code == 404:
            break
        r.raise_for_status()
        data = r.json()
        for ep in data["results"]:
            chars = ep["characters"]
            for a, b in combinations(sorted(chars), 2):
                pair_counts[(a, b)] += 1
        if page >= data["info"]["pages"]:
            break
        page += 1

    def get_character(url):
        if url not in character_cache:
            r = requests.get(url)
            r.raise_for_status()
            character_cache[url] = r.json()
        return character_cache[url]

    pairs = []
    for (a, b), count in pair_counts.items():
        if count < min:
            continue
        if max is not None and count > max:
            continue

        ca = get_character(a)
        cb = get_character(b)

        pairs.append({
            "character1": {"name": ca["name"], "url": ca["url"]},
            "character2": {"name": cb["name"], "url": cb["url"]},
            "episodes": count,
        })

    pairs.sort(key=lambda x: x["episodes"], reverse=True)
    return pairs[:limit]