from datetime import datetime, timedelta

from airflow.sdk import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from convert import ndjson_to_parquet


@dag(
    schedule=None, #'@daily', 
    start_date=datetime(2026, 10, 13, 1, 0),
    catchup=False,
)
def dag_ndjson_to_parquet_daily():

    @task
    def convert_files():
        """
        Читает все .ndjson из ndjson_path и записывает их в один .parquet
        """
        s3 = S3Hook(aws_conn_id="Silo_S3_connect")

        value_day = str(datetime.now().date() - timedelta(days=1))

        result = ndjson_to_parquet(
            s3=s3,
            bucket="data",
            source_prefix=f"prepared_json/auto.ru/{value_day}",
            target_key=f"prepared_parquet/auto.ru/{value_day}/data.parquet",
        )

        return result


    convert_files()

dag_ndjson_to_parquet_daily = dag_ndjson_to_parquet_daily()