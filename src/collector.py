import requests
import boto3

from datetime import datetime

from airflow.providers.amazon.aws.hooks.s3 import S3Hook    



def collect_data(params):

    s3 = S3Hook(aws_conn_id="Silo_S3_connect")
    headers = {"User-Agent": "Mozilla/5.0 ..."}

    url_template = params["url_template"]
    brand = params["brand"]
    page_from = params["page_from"]
    page_to = params["page_to"]

    for page in range(page_from, page_to + 1):

        url = url_template.format(
            brand=brand,
            page=page,
        )

        print(f"Downloading: {url}")

        response = requests.get(
            url,
            headers=headers
        )

        print("Uploading to Silo")

        s3.load_bytes(
            bucket_name="raw",
            key=f"auto.ru/bmw/{datetime.now().date()}/page-{page}.html",
            bytes_data=response.content,
        )

        print("File uploaded")

