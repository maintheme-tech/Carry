import requests
import boto3
from datetime import datetime


# Настройки
SOURCE = "auto.ru"
BRAND = "bmw"
BUCKET = "raw"


# Подключаемся к S3
s3 = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minioadmin",
    aws_secret_access_key="minioadmin",
    region_name="us-east-1",
)


def get_and_upload_page(page):
    # Формируем URL страницы
    url = f"https://auto.ru/cars/{BRAND}/all/?page={page}"

    # Получаем страницу
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    res = requests.get(url, headers=headers)

    print("Статус:", res.status_code)
    print("Размер:", len(res.content))

    # Формируем путь в S3
    now = datetime.now()

    date_path = now.strftime("%Y-%m-%d")
    time_path = now.strftime("%H%M%S")

    filename = f"page-{page:02d}_{time_path}.html"

    key = f"{SOURCE}/{BRAND}/{date_path}/{filename}"

    print("S3 key:", key)

    # Загружаем HTML в S3
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=res.content,
        ContentType="text/html",
    )

    print("HTML загружен в S3")



get_and_upload_page(1)