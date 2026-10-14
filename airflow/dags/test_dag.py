from airflow.sdk import dag, task

from datetime import datetime

from airflow.providers.trino.hooks.trino import TrinoHook


@dag(
    schedule=None,
    start_date=datetime(2026,10,7),
    catchup=False
)
def test_dag():

    @task
    def sync_partitions():

        trino = TrinoHook(trino_conn_id='Trino_connect')
        
        trino.run(sql="""
            CALL hive.system.sync_partition_metadata(
                schema_name => 'autoru_stg',
                table_name  => 'stg_autoru_listings',
                mode        => 'FULL'
            )
        """)

    sync_partitions()

test_dag = test_dag()