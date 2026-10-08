import boto3

from datetime import datetime
from urllib.request import Request, urlopen

from airflow.providers.amazon.aws.hooks.s3 import S3Hook


def collect_data(params, run_number):

    s3 = S3Hook(aws_conn_id="Silo_S3_connect")

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    url_template = params["url_template"]
    data_source = "auto.ru"  # TODO add dynamic data source
    brand = params["brand"]
    page_from = params["page_from"]
    page_to = params["page_to"]
    today = params["today"]

    bucket_name = "data"
    data_type = "raw"

    for page in range(page_from, page_to + 1):

        url = url_template.format(
            brand=brand,
            page=page,
        )

        print(f"Downloading: {url}")

        request = Request(
            url,
            headers=headers,
        )

        with urlopen(request, timeout=30) as response:

            if response.status != 200:
                raise RuntimeError(
                    f"Auto.ru returned HTTP {response.status}: {url}"
                )

            final_url = response.geturl()

            if "/showcaptcha" in final_url:
                raise RuntimeError(
                    f"Auto.ru returned CAPTCHA: {final_url}"
                )

            content = response.read()

        print(f"Uploading page-{page} to S3")

        s3.load_bytes(
            bucket_name=bucket_name,
            key=f"{data_type}/{data_source}/{brand}/{today}/{run_number}/page-{page}.html",
            bytes_data=content,
            replace=True,
        )

        print("File uploaded")

    return f"{data_type}/{data_source}/{brand}/{today}/{run_number}"