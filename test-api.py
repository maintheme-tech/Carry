import requests
from lxml import html

url = "https://auto.ru/cars/bmw/all/?page=1"

headers = {
    "User-Agent": "Mozilla/5.0"
}

res = requests.get(url, headers=headers)

tree = html.fromstring(res.content)

cards = tree.xpath('//div[contains(@class, "ListingItemUniversal")]')

url = cards[0].xpath(".//a/@href")[0]

auto_ru_id = url.rstrip("/").split("/")[-1].split("-")[0]

title = cards[0].xpath(
    ".//a[contains(@class, 'ListingItemTitle')]/text()"
)

title = title[0].replace("\xa0", " ").strip()

parts = title.split(",")

car_name = parts[0].strip()
year = int(parts[1].strip())
mileage = int(parts[2].replace("км", "").replace(" ", "").strip())

print("Автомобиль:", car_name)
print("Год:", year)
print("Пробег:", mileage)