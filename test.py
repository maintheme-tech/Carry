import time
import requests
from lxml import html


def download_page(page, filename):
    url = f"https://auto.ru/cars/bmw/all/?sort=cr_date-desc&page={page}"

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

from pathlib import Path


for i in range(1, 11):
    download_page(i, Path(f"parsedPages/a_test-{i}.html"))