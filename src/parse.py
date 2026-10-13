import io
import json
import pyarrow as pa
import pyarrow.parquet as pq

from pathlib import Path
from lxml import html

from airflow.providers.amazon.aws.hooks.s3 import S3Hook


# ---------------------------------------------------------------------------
# Хелперы
# ---------------------------------------------------------------------------

def clean_text(value):
    """Убирает nbsp и лишние пробелы."""
    return value.replace("\xa0", " ").strip() if value else None


def xpath_first(card, expr):
    """Первый непустой текст по xpath или None."""
    for raw in card.xpath(expr):
        text = clean_text(raw)
        if text:
            return text
    return None


def xpath_list(card, expr):
    """Список непустых текстов по xpath."""
    return [t for t in (clean_text(r) for r in card.xpath(expr)) if t]


def to_int(value, drop=("км", "₽", "\xa0", " ")):
    """Безопасный int: чистит единицы измерения, при ошибке — None."""
    if value is None:
        return None
    for token in drop:
        value = value.replace(token, "")
    try:
        return int(value.strip())
    except ValueError:
        return None


def parse_title(title):
    """'Model, Year, Mileage' → (model, year, mileage)."""
    parts = (title or "").split(",")
    model = parts[0].strip() if parts else None
    year = to_int(parts[1]) if len(parts) > 1 else None
    mileage = to_int(parts[2]) if len(parts) > 2 else None
    return model, year, mileage


# ---------------------------------------------------------------------------
# Парсинг одной карточки
# ---------------------------------------------------------------------------

def extract_card(tree, url):
    """Находит DOM-узел карточки по ссылке."""
    cards = tree.xpath(
        f"//a[@href='{url}']"
        "/ancestor::*[contains(@class, 'ListingItemUniversal-')][1]"
    )
    return cards[0] if cards else None


def parse_card(card, url):
    """Возвращает словарь с данными объявления или None."""

    # ID из ссылки
    auto_ru_id = url.rstrip("/").split("/")[-1].split("-")[0]

    # Заголовок: "Model, Year, Mileage"
    title = xpath_first(card, ".//a[contains(@class, 'ListingItemTitle__link')]/text()")
    if not title:
        return None
    model_title, year, mileage = parse_title(title)

    # Цена
    price = to_int(xpath_first(
        card,
        ".//div[contains(@class, 'ListingItemUniversalPrice__title')]//text()",
    ))

    # Характеристики: ["1.6 л, 75 л.с., бензин", body, drive, transmission]
    specs = xpath_list(
        card,
        ".//div[contains(@class, 'ListingItemUniversalSpecs__spec-')]/text()",
    )
    engine_parts = [clean_text(p) for p in specs[0].split(",")] if specs else []
    engine_volume = engine_parts[0] if len(engine_parts) > 0 else None
    power         = engine_parts[1] if len(engine_parts) > 1 else None
    fuel          = engine_parts[2] if len(engine_parts) > 2 else None
    body_type     = specs[1] if len(specs) > 1 else None
    drive         = specs[2] if len(specs) > 2 else None
    transmission  = specs[3] if len(specs) > 3 else None

    # Статус продажи
    condition = xpath_list(
        card,
        ".//*[contains(@class, 'ListingItemUniversalCondition__status-')]//text()",
    )
    sale_status = condition[1] if len(condition) > 1 else None

    # Цвет — последнее значение, кроме служебных
    colors = [
        c for c in xpath_list(
            card,
            ".//div[contains(@class, 'ListingItemUniversalSpecs__subtitle-')]//text()",
        )
        if c not in ("Комплектация", "•")
    ]
    color = colors[-1] if colors else None

    # Комплектация
    complectation = xpath_first(
        card,
        ".//*[contains(@class, 'ListingItemUniversalSpecs__complectationValue-')]/text()",
    )

    # Продавец
    seller             = xpath_first(card, ".//*[contains(@class, 'ListingItemUniversalSeller__sellerName-')]//text()")
    seller_profile_url = xpath_first(card, ".//a[contains(@class, 'ListingItemUniversalSeller__sellerName-')]/@href")
    seller_verified    = bool(card.xpath(".//*[contains(@class, 'ListingItemUniversalSeller__resellerVerifiedLabel-')]"))
    seller_rating      = xpath_first(card, ".//*[contains(@class, 'ListingItemUniversalSeller__resellerLabel-')]//text()")
    seller_region      = xpath_first(card, ".//span[contains(@class, 'MetroListPlace__regionName')]//text()")

    address_parts = card.xpath(
        ".//*[contains(@class, 'ListingItemUniversalSeller__sellerAddress-')]//text()"
    )
    seller_address = clean_text(" ".join(address_parts)) if address_parts else None

    # Фото и бейджи
    photo_urls = [u for u in card.xpath(".//img[contains(@class, 'LazyImage__image')]/@src") if u]
    badges     = xpath_list(card, ".//*[contains(@class, 'ListingItemUniversalBadges__badge-')]//text()")

    return {
        "auto_ru_id":         auto_ru_id,
        "url":                url,
        "model_title":        model_title,
        "year":               year,
        "mileage":            mileage,
        "price":              price,
        "engine_volume":      engine_volume,
        "power":              power,
        "fuel":               fuel,
        "body_type":          body_type,
        "drive":              drive,
        "transmission":       transmission,
        "sale_status":        sale_status,
        "color":              color,
        "complectation":      complectation,
        "seller":             seller,
        "seller_profile_url": seller_profile_url,
        "seller_verified":    seller_verified,
        "seller_rating":      seller_rating,
        "seller_region":      seller_region,
        "seller_address":     seller_address,
        "photo_count":        len(photo_urls),
        "photo_urls":         photo_urls,
        "badges":             badges,
    }



def parse_listings(file_path, params, run_number):
    bucket_name = "data"
    data_source = "auto.ru"  # TODO: сделать динамическим
    data_type   = "prepared_json"
    today       = params["today"]
    file_name   = Path(file_path).stem

    # Читаем HTML из S3
    s3 = S3Hook(aws_conn_id="Silo_S3_connect")
    content = s3.read_key(key=file_path, bucket_name=bucket_name)
    tree = html.fromstring(content)

    # Парсим все карточки
    links = tree.xpath("//a[contains(@class, 'ListingItemTitle__link')]/@href")

    listings = []
    for url in links:
        card = extract_card(tree, url)
        if card is None:
            continue
        listing = parse_card(card, url)
        if listing:
            listings.append(listing)


    ndjson_content = "\n".join(
        json.dumps(listing, ensure_ascii=False, default=str)
        for listing in listings
    )

    s3.load_string(
        string_data=ndjson_content,
        key= f"{data_type}/{data_source}/{today}/{run_number}__{file_name}.ndjson",
        bucket_name=f"{bucket_name}",
        replace=False
    ) 
