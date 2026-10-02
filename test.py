import time
import requests
from lxml import html


def download_page(page, filename):
    url = f"https://auto.ru/cars/bmw/1er/all/?sort=cr_date-desc&page={page}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    print("URL:", url)

    with open(filename, "wb") as f:
        f.write(res.content)

    return res.content

from lxml import html


def extract_ids_in_order(filename):
    with open(filename, "rb") as f:
        content = f.read()

    tree = html.fromstring(content)

    links = tree.xpath(
        "//a[contains(@class, 'ListingItemTitle__link')]/@href"
    )

    ids = []

    for url in links:
        auto_ru_id = (
            url.rstrip("/")
            .split("/")[-1]
            .split("-")[0]
        )

        ids.append(auto_ru_id)

    return ids


snapshots = {
    1: "page-1.html",
    2: "page-2-1.html",
    3: "page-3-1.html",
}

for snapshot, filename in snapshots.items():
    ids = extract_ids_in_order(filename)

    print(f"\n=== Снимок {snapshot} ===")

    for position, auto_ru_id in enumerate(ids, start=1):
        print(f"{position:02d}. {auto_ru_id}")