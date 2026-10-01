from lxml import html

with open("page.html", "rb") as f:
    content = f.read()

tree = html.fromstring(content)

cards = tree.xpath(
    '//div[contains(@class, "ListingItemUniversal")]'
)

print("Количество найденных элементов:", len(cards))