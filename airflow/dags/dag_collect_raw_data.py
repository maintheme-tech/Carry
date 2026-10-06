from datetime import datetime

from airflow.sdk import dag, task, get_current_context
from airflow.providers.standard.operators.trigger_dagrun import TriggerDagRunOperator

from collector import collect_data
from generator import generate_params


@dag(
    schedule=None,
    start_date=datetime(2026, 10, 5),
    catchup=False,
)
def dag_collect_raw_data():

    @task
    def download_pages():

        context = get_current_context()
        run_number = int(context["dag_run"].logical_date.strftime("%Y%m%d%H%M%S%f"))
        
        params = generate_params()

        collected_data_path = collect_data(params, run_number)

        return { "collected_data_path": collected_data_path }

    trigger_processor = TriggerDagRunOperator(
        task_id="trigger__dag_parse_collected_pages",
        trigger_dag_id="dag_parse_collected_pages",
        conf=download_pages(),
)


dag_collect_raw_data = dag_collect_raw_data()