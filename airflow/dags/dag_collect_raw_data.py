from datetime import datetime, timedelta

from airflow.sdk import dag, task, get_current_context
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

from generator import generate_params
from parser import collect_data


@dag(
    schedule=timedelta(minutes=20),
    start_date=datetime(2026, 10, 5),
    catchup=False,
)
def dag_collect_raw_data():

    @task(
        retries=2,
        retry_delay=timedelta(seconds=30),
    )
    def download_pages():

        context = get_current_context()
        run_number = context["dag_run"].logical_date.strftime("%Y%m%d%H%M%S")
        
        params = generate_params()

        collected_data_path = collect_data(params, run_number)

        return {
            "collected_data_path": collected_data_path,
            "params": params
        }

    trigger_processor = TriggerDagRunOperator(
        task_id="trigger__dag_process_collected_pages",
        trigger_dag_id="dag_process_collected_pages",
        conf=download_pages(),
)


dag_collect_raw_data = dag_collect_raw_data()