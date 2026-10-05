from datetime import datetime

from airflow.sdk import dag, task
from airflow.sdk import get_current_context

from collector import collect_data

@dag(
    schedule=None,
    start_date=datetime(2026, 10, 5),
    catchup=False,
)
def dag_collect_raw_data():

    @task
    def download_pages():

        context = get_current_context()
        params = context["dag_run"].conf

        collect_data(params)

    download_pages()


dag_collect_raw_data = dag_collect_raw_data()