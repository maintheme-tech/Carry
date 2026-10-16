import time
import requests
from lxml import html


def download_page(page, filename):
    import sys
    import ssl
    import requests
    import urllib3


    print("=== ENVIRONMENT ===")
    print("Python:", sys.version)
    print("OpenSSL:", ssl.OPENSSL_VERSION)
    print("requests:", requests.__version__)
    print("urllib3:", urllib3.__version__)

    print()
    print("=== PROXY ENV ===")

    import os

    for key in [
        "HTTP_PROXY",
        "HTTPS_PROXY",
        "ALL_PROXY",
        "http_proxy",
        "https_proxy",
        "all_proxy",
    ]:
        print(key, "=", os.environ.get(key))


    print()
    print("=== REQUEST ===")

    url = "https://auto.ru/cars/bmw/all/?sort=cr_date-desc"

    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    response = requests.get(
        url,
        headers=headers,
        allow_redirects=False,
    )

    print("status:", response.status_code)
    print("url:", response.url)
    print("location:", response.headers.get("Location"))
    print("content-type:", response.headers.get("Content-Type"))

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


import pendulum

print(pendulum.now('UTC'))
print()