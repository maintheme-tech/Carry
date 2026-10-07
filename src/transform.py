import json

from lxml import html
from pathlib import Path

from airflow.providers.amazon.aws.hooks.s3 import S3Hook    


def clean_text(value):
    if value is None:
        return None

    return (
        value
        .replace("\xa0", " ")
        .strip()
    )


def transform(file_path, params, run_number):

    url_template = params["url_template"]
    data_source = "auto.ru" # TODO add dynamic data source
    brand = params["brand"]
    page_from = params["page_from"]
    page_to = params["page_to"]
    today = params["today"]

    bucket_name = "data"
    data_type = "prepared"

    file_name = Path(file_path).stem

    s3 = S3Hook(aws_conn_id="Silo_S3_connect")

    content = s3.read_key(
        key=file_path,
        bucket_name=f"{bucket_name}",
    )

    print(content)

    tree = html.fromstring(content)

    links = tree.xpath(
        "//a[contains(@class, 'ListingItemTitle__link')]/@href"
    )

    listings = []

    for url in links:

        # -------------------------------------------------
        # ID объявления
        # -------------------------------------------------

        auto_ru_id = (
            url.rstrip("/")
            .split("/")[-1]
            .split("-")[0]
        )

        # -------------------------------------------------
        # КАРТОЧКА ОБЪЯВЛЕНИЯ
        # -------------------------------------------------

        cards = tree.xpath(
            f"//a[@href='{url}']"
            "/ancestor::*[contains(@class, 'ListingItemUniversal-')][1]"
        )

        if not cards:
            continue

        card = cards[0]

        # -------------------------------------------------
        # TITLE
        # -------------------------------------------------

        title_values = card.xpath(
            ".//a[contains(@class, 'ListingItemTitle__link')]/text()"
        )

        if not title_values:
            continue

        title = clean_text(title_values[0])

        parts = title.split(",")

        model_title = (
            parts[0].strip()
            if len(parts) > 0
            else None
        )

        year = None

        if len(parts) > 1:
            try:
                year = int(parts[1].strip())
            except ValueError:
                year = None

        mileage = None

        if len(parts) > 2:
            try:
                mileage = int(
                    parts[2]
                    .replace("км", "")
                    .replace("\xa0", "")
                    .replace(" ", "")
                    .strip()
                )
            except ValueError:
                mileage = None

        # -------------------------------------------------
        # PRICE
        # -------------------------------------------------

        price_values = card.xpath(
            ".//div[contains(@class, 'ListingItemUniversalPrice__title')]//text()"
        )

        price = None

        if price_values:
            try:
                price = int(
                    price_values[0]
                    .replace("\xa0", "")
                    .replace("₽", "")
                    .replace(" ", "")
                    .strip()
                )
            except ValueError:
                price = None

        # -------------------------------------------------
        # TECHNICAL SPECS
        # -------------------------------------------------

        specs = card.xpath(
            ".//div[contains(@class, 'ListingItemUniversalSpecs__spec-')]/text()"
        )

        specs = [
            clean_text(spec)
            for spec in specs
            if clean_text(spec)
        ]

        engine_volume = None
        power = None
        fuel = None

        if specs:

            engine_parts = [
                clean_text(x)
                for x in specs[0].split(",")
            ]

            if len(engine_parts) > 0:
                engine_volume = engine_parts[0]

            if len(engine_parts) > 1:
                power = engine_parts[1]

            if len(engine_parts) > 2:
                fuel = engine_parts[2]

        body_type = (
            specs[1]
            if len(specs) > 1
            else None
        )

        drive = (
            specs[2]
            if len(specs) > 2
            else None
        )

        transmission = (
            specs[3]
            if len(specs) > 3
            else None
        )

        # -------------------------------------------------
        # SALE STATUS
        # -------------------------------------------------

        condition_status = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalCondition__status-')]//text()"
        )

        condition_status = [
            clean_text(x)
            for x in condition_status
            if clean_text(x)
        ]

        sale_status = (
            condition_status[1]
            if len(condition_status) > 1
            else None
        )

        # -------------------------------------------------
        # COLOR
        # -------------------------------------------------

        color_values = card.xpath(
            ".//div[contains(@class, 'ListingItemUniversalSpecs__subtitle-')]//text()"
        )

        color_values = [
            clean_text(x)
            for x in color_values
            if clean_text(x)
        ]

        color_values = [
            x
            for x in color_values
            if x not in ("Комплектация", "•")
        ]

        color = (
            color_values[-1]
            if color_values
            else None
        )

        # -------------------------------------------------
        # КОМПЛЕКТАЦИЯ
        # -------------------------------------------------

        complectation_values = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalSpecs__complectationValue-')]/text()"
        )

        complectation = (
            clean_text(complectation_values[0])
            if complectation_values
            else None
        )

        # -------------------------------------------------
        # SELLER
        # -------------------------------------------------

        seller_values = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalSeller__sellerName-')]//text()"
        )

        seller = (
            clean_text(seller_values[0])
            if seller_values
            else None
        )

        # -------------------------------------------------
        # SELLER PROFILE URL
        # -------------------------------------------------

        seller_profile_values = card.xpath(
            ".//a[contains(@class, 'ListingItemUniversalSeller__sellerName-')]/@href"
        )

        seller_profile_url = (
            seller_profile_values[0]
            if seller_profile_values
            else None
        )

        # -------------------------------------------------
        # ПРОВЕРЕННЫЙ ПРОДАВЕЦ
        # -------------------------------------------------

        seller_verified = bool(
            card.xpath(
                ".//*[contains(@class, 'ListingItemUniversalSeller__resellerVerifiedLabel-')]"
            )
        )

        # -------------------------------------------------
        # РЕЙТИНГ ПРОДАВЦА
        # -------------------------------------------------

        seller_rating_values = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalSeller__resellerLabel-')]//text()"
        )

        seller_rating_values = [
            clean_text(x)
            for x in seller_rating_values
            if clean_text(x)
        ]

        seller_rating = (
            seller_rating_values[0]
            if seller_rating_values
            else None
        )

        # -------------------------------------------------
        # REGION
        # -------------------------------------------------

        seller_region_values = card.xpath(
            ".//span[contains(@class, 'MetroListPlace__regionName')]//text()"
        )

        seller_region = (
            clean_text(seller_region_values[0])
            if seller_region_values
            else None
        )

        # -------------------------------------------------
        # ADDRESS
        # -------------------------------------------------

        seller_address_values = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalSeller__sellerAddress-')]//text()"
        )

        seller_address = (
            clean_text(" ".join(seller_address_values))
            if seller_address_values
            else None
        )

        # -------------------------------------------------
        # PHOTOS
        # -------------------------------------------------

        photo_urls = card.xpath(
            ".//img[contains(@class, 'LazyImage__image')]/@src"
        )

        photo_urls = [
            photo_url
            for photo_url in photo_urls
            if photo_url
        ]

        photo_count = len(photo_urls)

        # -------------------------------------------------
        # BADGES
        # -------------------------------------------------

        badges = card.xpath(
            ".//*[contains(@class, 'ListingItemUniversalBadges__badge-')]//text()"
        )

        badges = [
            clean_text(badge)
            for badge in badges
            if clean_text(badge)
        ]

        # -------------------------------------------------
        # RESULT
        # -------------------------------------------------

        listings.append({
            "auto_ru_id": auto_ru_id,
            "url": url,
            "model_title": model_title,
            "year": year,
            "mileage": mileage,
            "price": price,
            "engine_volume": engine_volume,
            "power": power,
            "fuel": fuel,
            "body_type": body_type,
            "drive": drive,
            "transmission": transmission,
            "sale_status": sale_status,
            "color": color,
            "complectation": complectation,
            "seller": seller,
            "seller_profile_url": seller_profile_url,
            "seller_verified": seller_verified,
            "seller_rating": seller_rating,
            "seller_region": seller_region,
            "seller_address": seller_address,
            "photo_count": photo_count,
            "photo_urls": photo_urls,
            "badges": badges,
        })


    json_content = json.dumps(listings, indent=2)

    s3.load_string(
        string_data=json_content,
        key= f"{data_type}/{data_source}/{brand}/{today}/{run_number}/{file_name}.json",
        bucket_name=f"{bucket_name}",
        replace=True
    )    


