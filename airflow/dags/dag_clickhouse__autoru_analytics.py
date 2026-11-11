import base64
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.sdk import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


LOGGER = logging.getLogger(__name__)
SQL_PATH = Path("/opt/airflow/sql/scripts/clickhouse_load_analytics_snapshot.sql")


def _clickhouse_endpoint(connection) -> str:
    if not connection.host:
        raise ValueError("Airflow connection ClickHouse_connect must define a host")

    raw_host = connection.host.strip()
    parsed_host = urlsplit(raw_host if "://" in raw_host else "")
    scheme = parsed_host.scheme or (
        connection.schema if connection.schema in {"http", "https"} else "http"
    )
    hostname = parsed_host.hostname or raw_host
    port = connection.port or parsed_host.port or 8123
    return f"{scheme}://{hostname}:{port}/"


def _sql_string(value: str) -> str:
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def _split_statements(sql: str) -> list[str]:
    statements = []
    start = 0
    quote = None
    line_comment = False
    block_comment = False
    has_sql = False
    index = 0

    while index < len(sql):
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < len(sql) else ""

        if line_comment:
            if char == "\n":
                line_comment = False
        elif block_comment:
            if char == "*" and next_char == "/":
                block_comment = False
                index += 1
        elif quote:
            if char == "\\":
                index += 1
            elif char == quote:
                if next_char == quote:
                    index += 1
                else:
                    quote = None
        elif char == "-" and next_char == "-":
            line_comment = True
            index += 1
        elif char == "/" and next_char == "*":
            block_comment = True
            index += 1
        elif char in {"'", '"', "`"}:
            quote = char
            has_sql = True
        elif char == ";":
            if has_sql:
                statements.append(sql[start:index].strip())
            start = index + 1
            has_sql = False
        elif not char.isspace():
            has_sql = True

        index += 1

    if quote or block_comment:
        raise ValueError("Unterminated quoted string or block comment in ClickHouse SQL")

    if has_sql:
        statements.append(sql[start:].strip())
    return statements


def _render_sql(
    sql: str,
    snapshot_date: date,
    iceberg_url: str,
    access_key: str,
    secret_key: str,
) -> str:
    replacements = {
        "{snapshot_date:Date}": f"toDate({_sql_string(snapshot_date.isoformat())})",
        "{iceberg_url:String}": _sql_string(iceberg_url),
        "{s3_access_key_id:String}": _sql_string(access_key),
        "{s3_secret_access_key:String}": _sql_string(secret_key),
    }
    for placeholder, value in replacements.items():
        sql = sql.replace(placeholder, value)

    unresolved = [placeholder for placeholder in replacements if placeholder in sql]
    if unresolved:
        raise ValueError(f"Unresolved ClickHouse SQL parameters: {unresolved}")
    return sql


@dag(
    schedule=None,
    start_date=datetime(2026, 10, 15),
    catchup=False,
    max_active_runs=1,
    tags=["clickhouse", "analytics", "autoru"],
)
def dag_clickhouse__autoru_analytics():
    @task(retries=2, retry_delay=timedelta(minutes=5))
    def load_analytics_snapshot(**context):
        run_conf = context["dag_run"].conf or {}
        raw_snapshot_date = run_conf.get("snapshot_date")
        if not isinstance(raw_snapshot_date, str):
            raise ValueError("DAG run conf must include snapshot_date as YYYY-MM-DD")

        try:
            snapshot_date = date.fromisoformat(raw_snapshot_date)
        except ValueError as error:
            raise ValueError("snapshot_date must use YYYY-MM-DD format") from error
        if snapshot_date.isoformat() != raw_snapshot_date:
            raise ValueError("snapshot_date must use YYYY-MM-DD format")

        iceberg_url = Variable.get("clickhouse_iceberg_actual_listings_url")
        s3_credentials = S3Hook(aws_conn_id="Silo_S3_connect").get_credentials()
        if (
            not s3_credentials
            or not s3_credentials.access_key
            or not s3_credentials.secret_key
        ):
            raise ValueError("Silo_S3_connect must provide S3 access and secret keys")

        clickhouse_connection = BaseHook.get_connection("ClickHouse_connect")
        endpoint = _clickhouse_endpoint(clickhouse_connection)
        sql = SQL_PATH.read_text(encoding="utf-8")
        sql = _render_sql(
            sql,
            snapshot_date,
            iceberg_url,
            s3_credentials.access_key,
            s3_credentials.secret_key,
        )
        statements = _split_statements(sql)
        if not statements:
            raise ValueError(f"No SQL statements found in {SQL_PATH}")

        headers = {"Content-Type": "text/plain; charset=utf-8"}
        if clickhouse_connection.login:
            credentials = (
                f"{clickhouse_connection.login}:"
                f"{clickhouse_connection.password or ''}"
            )
            encoded_credentials = base64.b64encode(
                credentials.encode("utf-8")
            ).decode("ascii")
            headers["Authorization"] = f"Basic {encoded_credentials}"

        for statement_number, statement in enumerate(statements, start=1):
            request = Request(
                f"{endpoint}?mutations_sync=2&wait_end_of_query=1",
                data=statement.encode("utf-8"),
                headers=headers,
                method="POST",
            )
            try:
                with urlopen(request, timeout=1800) as response:
                    response.read()
            except HTTPError as error:
                raise RuntimeError(
                    f"ClickHouse returned HTTP {error.code} for statement "
                    f"{statement_number}/{len(statements)} while loading "
                    f"snapshot {snapshot_date}"
                ) from error
            except URLError as error:
                raise RuntimeError(
                    f"Could not connect to ClickHouse at {endpoint}"
                ) from error

        LOGGER.info("Loaded ClickHouse analytics snapshot for %s", snapshot_date)

    load_analytics_snapshot()

dag_clickhouse__autoru_analytics = dag_clickhouse__autoru_analytics()
