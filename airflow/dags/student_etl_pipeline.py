from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import os

default_args = {"owner": "tejas", "retries": 1}

# ✅ correct path — data folder inside dags
DATA_DIR = "/opt/airflow/dags/data"

def extract():
    # read students.csv
    df = pd.read_csv(f"{DATA_DIR}/students.csv")

    # print shape
    print(f"Shape: {df.shape}")

    # print first 5 rows
    print("First 5 rows:")
    print(df.head())

    # print null counts
    print("Null counts:")
    print(df.isnull().sum())

with DAG(
    dag_id="student_etl_pipeline",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["practice", "students"],
) as dag:

    extract_task = PythonOperator(
        task_id="extract",
        python_callable=extract,
    )