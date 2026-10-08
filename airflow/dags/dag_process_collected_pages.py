from datetime import datetime

from airflow.sdk import dag, task, get_current_context
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from transform import transform


@dag(
    schedule=None,
    start_date=datetime(2026,10,6),
    catchup=False
)
def dag_process_collected_pages():

    s3 = S3Hook(aws_conn_id="Silo_S3_connect")

    @task
    def get_file_paths():

        context = get_current_context()

        files = s3.list_keys(
            bucket_name="data",
            prefix=context["dag_run"].conf["collected_data_path"],
        )

        return files
        
    @task
    def transform_page(file_path):

        context = get_current_context()
        params = context["dag_run"].conf["params"]
        run_number = context["dag_run"].logical_date.strftime("%Y%m%d%H%M%S")

        print(f"Processing {file_path}")

        listings = transform(file_path, params, run_number)

        return run_number

    file_paths = get_file_paths()
    transform_page.expand(file_path=file_paths)

dag_process_collected_pages = dag_process_collected_pages()