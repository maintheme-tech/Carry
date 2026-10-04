from airflow.sdk import dag, task
from datetime import datetime


@dag(
    schedule = None,
    catchup = False,
    start_date = datetime(2026, 10, 2)
)
def test_decorator_dag():
    
    @task
    def generate_numbers():
        return [10, 20, 30, 40]
    
    @task
    def calculate_sum(nums):
        return sum(nums)

    @task
    def print_result(num):
        print(f"The sum is {num}")

    
    print_result(calculate_sum(generate_numbers()))


test_dag = test_decorator_dag()
