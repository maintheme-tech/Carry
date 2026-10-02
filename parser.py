from lxml import html

def parse_listings(content):
    tree = html.fromstring(content)

    links = tree.xpath(
        "//a[contains(@class, 'ListingItemTitle__link')]/@href"
    )

    listings = []

    for url in links:
        auto_ru_id = (
            url.rstrip("/")
            .split("/")[-1]
            .split("-")[0]
        )

        card = tree.xpath(
            f"//a[@href='{url}']"
        )[0]

        for i in range(6):
            card = card.getparent()

        title = card.xpath(
            ".//a[contains(@class, 'ListingItemTitle__link')]/text()"
        )[0].replace('\xa0', '').strip()
        parts = title.split(',')
        model_title, year, mileage = parts[0], int(parts[1].strip()), int(parts[2].replace('км', '').strip())

        price = card.xpath(
            ".//div[contains(@class, 'ListingItemUniversalPrice__title')]//text()"
        )[0].replace('\xa0', '').strip()
        price = int(price.replace('₽', '').replace(' ', ''))

        engine = card.xpath(
            ".//div[contains(@class, 'ListingItemUniversalSpecs__spec-')]/text()"
        )[0].replace('\xa0', '').strip()
        parts = engine.split(',')
        engine, power = parts[0] + ' ' + parts[2], parts[1]

        listings.append({
            "auto_ru_id": auto_ru_id,
            "url": url,
            "model_title": model_title,
            "year": year,
            "mileage": mileage,
            "price": price,
            "engine": engine,
            "power": power
        })

    return listings


with open("page-1.html", "rb") as f:
    content = f.read()

listings = (parse_listings(content))

for listing in listings:
    for key, value in listing.items():
        print('\''+key+'\''+':', value)
    print()