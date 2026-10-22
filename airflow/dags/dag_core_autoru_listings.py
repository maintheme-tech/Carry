import pendulum

from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.trino.hooks.trino import TrinoHook

from common.upload.delta_loader import DeltaLoaderOperator
from common.upload.core_loader import LoadCoreTableOperator

local_tz = pendulum.timezone("Europe/Moscow")

@dag(
    schedule=None,
    start_date=datetime(2026, 10, 15),
    catchup=False,
    template_searchpath='/opt/airflow/include'
)
def dag_core_autoru_listings():

    trino = TrinoHook(trino_conn_id='Trino_connect')

    @task(
        multiple_outputs=True
    )
    def get_context_params(**context):
        return {
            'value_day': context['logical_date']
                .in_timezone('Europe/Moscow')
                .subtract(days=1)
                .to_date_string(),
            'job_id': int(context['logical_date'].strftime('%Y%m%d%H%M%S'))
        }

    params = get_context_params()

    load_delta = DeltaLoaderOperator(
        task_id="load_delta",
        p_hook=trino,   
        p_source_schema = 'hive.autoru_raw',
        p_source_table = 'raw_autoru_listings',
        p_target_schema = 'iceberg.autoru_stg',
        p_target_table = 'stg_autoru_listings',
        p_sql_query = "script_autoru_stg__stg_autoru_listings.sql",
        p_value_day = params['value_day'],
        p_as_of_day = pendulum.now('Europe/Moscow').start_of('second'),
        p_job_id = params['job_id'],
        p_drop_duplicates = False,
        p_gather_stats = True
    )

    upload_target = LoadCoreTableOperator(
        task_id="load_target",
        p_hook=trino,
        p_source_schema='iceberg.autoru_stg',
        p_source_table='stg_autoru_listings',
        p_target_schema='iceberg.autoru_core',
        p_target_table='core_autoru_actual_listings',
        p_as_of_day=pendulum.now('Europe/Moscow').start_of('second'),
        p_drop_duplicates=True,
        p_gather_stats=True
    )


    params >> load_delta >> upload_target

dag_core_autoru_listings = dag_core_autoru_listings()