from airflow.sdk import dag, task

from datetime import datetime

from airflow.providers.trino.hooks.trino import TrinoHook
import pendulum

@dag(
    schedule=None,
    start_date=datetime(2026,10,7),
    catchup=False
)
def test_dag():

    hook = TrinoHook(trino_conn_id="Trino_connect")

    @task
    def test_task(**context):

        print(int(context["logical_date"].strftime("%Y%m%d%H%M%S")))

    test_task()

test_dag = test_dag()