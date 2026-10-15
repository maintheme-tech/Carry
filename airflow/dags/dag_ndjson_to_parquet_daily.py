import pendulum

from datetime import datetime, timedelta

from airflow.sdk import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.trino.hooks.trino import TrinoHook

from convert import ndjson_to_parquet

local_tz = pendulum.timezone("Europe/Moscow")

@dag(
    schedule=None, #'@daily', 
    start_date=pendulum.datetime(2026, 10, 13, 0, 3, tz=local_tz),
    catchup=False,
)
def dag_ndjson_to_parquet_daily():

    @task
    def convert_files(data_interval_start=None):

        s3 = S3Hook(aws_conn_id="Silo_S3_connect")

        value_day = (
            data_interval_start
            .in_timezone(local_tz)
            .subtract(days=1)
            .strftime("%Y-%m-%d")
        )

        ndjson_to_parquet(
            s3=s3,
            bucket="data",
            source_prefix=f"prepared_json/auto.ru/{value_day}",
            target_key=f"prepared_parquet/auto.ru/value_day={value_day}/data.parquet",
            value_day=value_day
        )

    @task
    def sync_partitions():

        trino = TrinoHook(trino_conn_id='Trino_connect')
        
        trino.run(sql="""
            CALL hive.system.sync_partition_metadata(
                schema_name => 'autoru_raw',
                table_name  => 'raw_autoru_listings',
                mode        => 'FULL'
            )
        """)


    convert_files() >> sync_partitions()

dag_ndjson_to_parquet_daily = dag_ndjson_to_parquet_daily()