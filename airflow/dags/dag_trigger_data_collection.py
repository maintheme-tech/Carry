from datetime import datetime

from airflow.sdk import dag, task
from airflow.operators.trigger_dagrun import TriggerDagRunOperator

from generator import generate_params


@dag(
    schedule=None,
    start_date=datetime(2025, 10, 5), 
    catchup=False
)
def dag_trigger_data_collection():

    params = generate_params()

    trigger = TriggerDagRunOperator(
        task_id='trigger_collect_raw_data',
        trigger_dag_id='dag_collect_raw_data',
        conf=params
    )


dag_trigger_data_collection = dag_trigger_data_collection()