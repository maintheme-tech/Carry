import pendulum

from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.trino.hooks.trino import TrinoHook


@dag(
    schedule=None,
    start_date=datetime(2026, 10, 15),
    catchup=False
)
def dag_iceberg_stg__stg_autoru_listings():

    trino = TrinoHook(trino_conn_id='Trino_connect')

    @task
    def count_rows_to_insert():