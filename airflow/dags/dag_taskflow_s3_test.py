import boto3
import json

from airflow.sdk import dag, task
from datetime import datetime


@dag(
    schedule=None,
    start_date=datetime(2026, 10, 4),
    catchup=False
)
def S3_taskflow_test_dag():

    # Подключаемся к S3
    s3 = boto3.client(
        "s3",
        endpoint_url="http://silo-iceberg:9000",
        aws_access_key_id="minioadmin",
        aws_secret_access_key="minioadmin",
        region_name="us-east-1",
    )

    bucket = "test"
    key = "numbers.json"

    @task
    def generate_numbers():
        numbers = list(range(1001))

        # Загружаем HTML в S3
        s3.put_object(
            Bucket=bucket,
            Key=key,
            Body=json.dumps(numbers),
            ContentType="application/json",
        )

        return f"s3://{bucket}/{key}"

    @task
    def calculate_stats(S3_path):

        response = s3.get_object(
                Bucket=bucket,
                Key=key
            )
            
        data = response["Body"].read()

        numbers = json.loads(data)

        print(numbers)
    
        return max(numbers), min(numbers)


    calculate_stats(generate_numbers())


S3_taskflow_test_dag = S3_taskflow_test_dag()