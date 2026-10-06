from datetime import datetime

from airflow.sdk import dag, task, get_current_context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from parser import parse


@dag(
    schedule=None,
    start_date=datetime(2026,10,6),
    catchup=False
)
def dag_parse_collected_pages():

    s3 = S3Hook(aws_conn_id="Silo_S3_connect")

    @task
    def get_file_paths():

        context = get_current_context()

        files = s3.list_keys(
            bucket_name="test",
            prefix=context["dag_run"].conf["collected_data_path"],
        )

        return files
        
    @task
    def parse_page(file_path):

        html = s3.read_key(
            key=file_path,
            bucket_name="data",
        )

        print(f"Parsing {file_path}")


        return ...
