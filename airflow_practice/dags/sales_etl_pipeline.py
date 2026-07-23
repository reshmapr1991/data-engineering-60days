from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import numpy as np

default_args = {"owner": "tejas", "retries": 1}
DATA_DIR = "/opt/airflow/dags/data"

def extract():
    df = pd.read_csv(f"{DATA_DIR}/sales.csv")
    print(f"Shape: {df.shape}")
    print(f"Null count: {df.isnull().sum().sum()}")
    print(df.head())
    df.to_csv(f"{DATA_DIR}/sales_extracted.csv", index=False)
    print("Saved sales_extracted.csv")

def clean():
    df = pd.read_csv(f"{DATA_DIR}/sales_extracted.csv")
    df["salesperson"] = df["salesperson"].str.strip().str.title()
    df["quantity"] = df["quantity"].fillna(df["quantity"].median())
    df = df[df["quantity"] > 0]
    print(f"Rows after cleaning: {len(df)}")
    df.to_csv(f"{DATA_DIR}/sales_cleaned.csv", index=False)
    print("Saved sales_cleaned.csv")

def transform():
    df = pd.read_csv(f"{DATA_DIR}/sales_cleaned.csv")
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.month_name()
    print(f"Total orders: {len(df)}")
    df.to_csv(f"{DATA_DIR}/transform_csv.csv", index=False)
    print("Saved transform_csv.csv")

def analyse():
    df = pd.read_csv(f"{DATA_DIR}/transform_csv.csv")

    total_revenue    = df.groupby("region")["revenue"].sum()
    total_product    = df.groupby("product")["quantity"].sum()
    top_salesperson  = df.groupby("salesperson")["revenue"].sum()
    payment_revenue  = df.groupby("payment_mode")["revenue"].sum().sort_values(ascending=False)
    best_payment     = payment_revenue.idxmax()
    completed_orders = len(df[df["status"] == "completed"])
    returned_orders  = len(df[df["status"] == "returned"])
    cancelled_orders = len(df[df["status"] == "cancelled"])
    total_rev_sum    = df["revenue"].sum()
    avg_order_val    = df["revenue"].mean().round(0)

    print("="*50)
    print("SALES PERFORMANCE REPORT".center(50))
    print("="*50)
    print(f"Total orders        : {len(df)}")
    print(f"Completed orders    : {completed_orders}")
    print(f"Cancelled orders    : {cancelled_orders}")
    print(f"Returned orders     : {returned_orders}")
    print("-"*50)
    print(f"Total revenue       : {total_rev_sum:,}")
    print(f"Average order value : {avg_order_val:,}")
    print("-"*50)
    print(f"Top region          : {total_revenue.idxmax()}")
    print(f"Top product         : {total_product.idxmax()}")
    print(f"Top salesperson     : {top_salesperson.idxmax()}")
    print("-"*50)
    print(f"Best payment mode   : {best_payment}")
    print("Revenue by payment mode:")
    for mode, rev in payment_revenue.items():
        print(f"  {mode}: {rev:,}")
    print("="*50)

with DAG(
    dag_id="sales_etl_pipeline",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["sales", "practice"],
) as dag:
    t1 = PythonOperator(task_id="extract",   python_callable=extract)
    t2 = PythonOperator(task_id="clean",     python_callable=clean)
    t3 = PythonOperator(task_id="transform", python_callable=transform)
    t4 = PythonOperator(task_id="analyse",   python_callable=analyse)
    t1 >> t2 >> t3 >> t4
