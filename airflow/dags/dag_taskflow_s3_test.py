import json

from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


@dag(
    schedule=None,
    start_date=datetime(2026, 10, 4),
    catchup=False
)
def S3_taskflow_test_dag():

    @task
    def test_s3():

        s3 = S3Hook(aws_conn_id="Silo_S3_connect")

        print(s3.check_for_bucket("raw"))


    test_s3()


S3_taskflow_test_dag = S3_taskflow_test_dag()