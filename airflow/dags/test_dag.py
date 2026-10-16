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

    @task
    def test_task(**context):


        print(context['logical_date'].in_timezone('Europe/Moscow').to_date_string())


    test_task()

test_dag = test_dag()