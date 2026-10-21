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

        print(f'run_id = {context['run_id']}, task = {context['task']}, task_instance = {context['task_instance']},ti = {context['ti']}, dag_run = {context['dag_run']}' )


    test_task()

test_dag = test_dag()