from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "owner": "tejas",
    "retries": 1,
    "retry_delay": timedelta(minutes=1),
}

def extract_data():
    print("Extracting data from source...")
    print("Found 100 records")
    return "extraction_complete"

def transform_data():
    print("Transforming data...")
    print("Cleaned and formatted 100 records")
    return "transform_complete"

def load_data():
    print("Loading data to warehouse...")
    print("Loaded 100 records successfully")
    return "load_complete"

with DAG(
    dag_id="my_first_etl_pipeline",
    default_args=default_args,
    description="My first ETL pipeline in Airflow",
    schedule_interval="@daily",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["learning", "day9"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract_data",
        python_callable=extract_data,
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=load_data,
    )

    notify_task = BashOperator(
        task_id="notify_success",
        bash_command='echo "Pipeline completed successfully at $(date)"',
    )

    extract_task >> transform_task >> load_task >> notify_task
