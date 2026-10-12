from airflow.sdk import dag, task

from datetime import datetime

from transform import transform_json


@dag(
    schedule=None,
    start_date=datetime(2026,10,7),
    catchup=False
)
def test_dag():

    @task
    def merge_json(json_storage_path, parquet_file_location):
        
        transform_json(json_storage_path, parquet_file_location)


    merge_json('data/prepared/auto.ru/2026-10-10', f'data/warehouse/raw/{str(datetime.now().date())}.parquet')

test_dag = test_dag()