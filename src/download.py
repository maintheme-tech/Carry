import random
import time

from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

# ---------------------------------------------------------------------------
# Константы
# ---------------------------------------------------------------------------

BUCKET_NAME = "data"
DATA_TYPE   = "raw"
DATA_SOURCE = "auto.ru"  # TODO: сделать динамическим
HEADERS     = {"User-Agent": "Mozilla/5.0"}
TIMEOUT_SEC = 15

# Троттлинг: пауза между страницами (сек)
THROTTLE_MIN = 1.0
THROTTLE_MAX = 2.5

# Ретраи: сколько попыток и как ждать между ними
RETRY_ATTEMPTS   = 5
RETRY_WAIT_MIN   = 2   # начальная пауза, сек
RETRY_WAIT_MAX   = 30  # максимальная пауза, сек


# ---------------------------------------------------------------------------
# Сетевые ошибки, которые имеет смысл ретраить
# ---------------------------------------------------------------------------

class RetryableFetchError(Exception):
    """Временная ошибка сети/сервера — повторяем."""


class CaptchaError(Exception):
    """Капча — повторять бессмысленно, нужно вмешательство."""


# ---------------------------------------------------------------------------
# Загрузка одной страницы (с ретраями)
# ---------------------------------------------------------------------------

@retry(
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=RETRY_WAIT_MIN, max=RETRY_WAIT_MAX),
    retry=retry_if_exception_type(RetryableFetchError),
    reraise=True,
)
def fetch_page_content(url):
    """Скачивает HTML по URL, ретраит временные сбои."""
    request = Request(url, headers=HEADERS)

    try:
        with urlopen(request, timeout=TIMEOUT_SEC) as response:
            final_url = response.geturl()

            # Капча — не ретраим, сразу падаем
            if "/showcaptcha" in final_url:
                raise CaptchaError(f"Auto.ru returned CAPTCHA: {final_url}")

            # 5xx и 429 — временные, ретраим
            if response.status >= 500 or response.status == 429:
                raise RetryableFetchError(
                    f"Auto.ru returned HTTP {response.status}: {url}"
                )

            # Остальные не-200 — сразу падаем
            if response.status != 200:
                raise RuntimeError(
                    f"Auto.ru returned HTTP {response.status}: {url}"
                )

            return response.read()

    except HTTPError as e:
        # HTTPError — это ответ с кодом 4xx/5xx
        if e.code >= 500 or e.code == 429:
            raise RetryableFetchError(f"HTTP {e.code}: {url}") from e
        raise RuntimeError(f"HTTP {e.code}: {url}") from e

    except URLError as e:
        # Сетевые сбои (DNS, timeout, connection reset)
        raise RetryableFetchError(f"Network error: {e.reason} ({url})") from e



def download_pages(params, run_number):
    s3 = S3Hook(aws_conn_id="Silo_S3_connect")

    url_template = params["url_template"]
    brand        = params["brand"]
    page_from    = params["page_from"]
    page_to      = params["page_to"]
    today        = params["today"]

    prefix = f"{DATA_TYPE}/{DATA_SOURCE}/{today}/{run_number}"

    for page in range(page_from, page_to + 1):
        url = url_template.format(brand=brand, page=page)
        print(f"Downloading: {url}")

        content = fetch_page_content(url)

        key = f"{prefix}/page-{page}.html"
        print(f"Uploading {key} to S3")

        s3.load_bytes(
            bucket_name=BUCKET_NAME,
            key=key,
            bytes_data=content,
            replace=True,
        )

        # Пауза перед следующей страницей, чтобы не злить auto.ru
        if page < page_to:
            time.sleep(random.uniform(THROTTLE_MIN, THROTTLE_MAX))

    return prefix