import pendulum

from datetime import datetime

from airflow.sdk import dag, task
from airflow.providers.trino.hooks.trino import TrinoHook

from common.upload.delta_loader import DeltaLoaderOperator
from common.helper.run_sql_query import RunSQLQueryOperator
from common.upload.history_loader import LoadHistTableOperator


@dag(
    schedule=None,
    catchup=False,
    start_date=datetime(2026, 11, 1),
    template_searchpath='/opt/airflow/include'
)
def dag_autoru_core__listings_history():
    
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

    task_fill_proc_active_listings = RunSQLQueryOperator(
            task_id='task_fill_proc_active_listings',
            p_sql_query_path='script_autoru_stg__proc_active_listings.sql',
            p_hook=trino
    )

    task_fill_proc_new_listings = RunSQLQueryOperator(
        task_id='task_fill_proc_new_listings',
        p_sql_query_path='script_autoru_stg__proc_new_listings.sql',
        p_hook=trino
    )

    task_fill_proc_deleted_listings = RunSQLQueryOperator(
        task_id='task_fill_proc_deleted_listings',
        p_sql_query_path='script_autoru_stg__proc_deleted_listings.sql',
        p_hook=trino
    )

    task_fill_proc_updated_listings = RunSQLQueryOperator(
        task_id='task_fill_proc_updated_listings',
        p_sql_query_path='script_autoru_stg__proc_updated_listings.sql',
        p_hook=trino
    )

    task_fill_proc_batch_listings = RunSQLQueryOperator(
        task_id='task_fill_proc_batch_listings',
        p_sql_query_path='script_autoru_stg__proc_batch_listings.sql',
        p_hook=trino
    )

    upload_target = LoadHistTableOperator(
        task_id='upload_target',
        p_hook=trino,
        p_source_schema='iceberg.autoru_stg',
        p_source_table='proc_batch_listings',
        p_target_schema='iceberg.autoru_core',
        p_target_table='listings_history',
        p_as_of_day=pendulum.now('Europe/Moscow').start_of('second')
    )


    params >> [load_delta, task_fill_proc_active_listings] >> task_fill_proc_new_listings >> task_fill_proc_deleted_listings >> task_fill_proc_updated_listings >> task_fill_proc_batch_listings >> upload_target

dag_autoru_core__listings_history = dag_autoru_core__listings_history()