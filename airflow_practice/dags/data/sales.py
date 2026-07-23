from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import numpy as np
import pandas as pd
import os

default_args= {"owner" : "tejas", "retries":1}

DATA_DIR="/opt/airflow/dags/data"
def extract():
   df =pd.read_csv(f"{DATA_DIR}/sales.csv")

   # print table
   print(df)

   # print first 5 rows
   print(f"Head: {df.head()}")

   # print shape
   print(f"Shape:{df.shape}")

   #null counts
   print(f"Null count: {df.isnull().sum()}")

   df.to_csv(f"{DATA_DIR}/sales_extracted.csv",index=False)
   print("Saved Extracted csv")

def clean():

   df = pd.read_csv(f"{DATA_DIR}/sales_extracted.csv")
   df["salesperson"] =df["salesperson"].str.strip().str.title()

   df = df[df["quantity"] > 0]
   df["quantity"]=df["quantity"].fillna(df["quantity"].median())

   df.to_csv(f"{DATA_DIR}/sales_cleaned.csv",index=False)
   print("Saved Extracted csv")

   return df


def transform():
   df = pd.read_csv(f"{DATA_DIR}/sales_cleaned.csv")
   df["revenue"] = df["quantity"] * df["unit_price"]
   df["order_date"] = pd.to_datetime(df["order_date"])
   df["month"] = df["order_date"].dt.month_name()

   # save ALL orders with revenue column
   df.to_csv(f"{DATA_DIR}/transform_csv.csv", index=False)

   # also save completed separately if needed
   completed = df[df["status"] == "completed"]
   print(f"Total orders    : {len(df)}")
   print(f"Completed orders: {len(completed)}")
   print("Saved transform_csv.csv")

def analyse():
   df = pd.read_csv(f"{DATA_DIR}/transform_csv.csv")

   # calculate all metrics first
   print(f"Rows in transform_csv: {len(df)}")
   total_revenue = df.groupby("region")["revenue"].sum()
   total_product = df.groupby("product")["quantity"].sum()
   top_salesperson = df.groupby("salesperson")["revenue"].sum()
   completed_orders = len(df[df["status"] == "completed"])
   returned_orders = len(df[df["status"] == "returned"])
   cancelled_orders = len(df[df["status"] == "cancelled"])
   total_rev_sum = df["revenue"].sum()
   avg_order_val = df["revenue"].mean().round(0)
   # ✅ show all payment modes with revenue
   payment_revenue = df.groupby("payment_mode")["revenue"].sum().sort_values(ascending=False)
   print("Revenue by payment mode:")
   for mode, rev in payment_revenue.items():
      print(f"  {mode}: ₹{rev:,}")
   best_payment = payment_revenue.idxmax()
   print(f"Best payment mode : {best_payment}")



   # print report FIRST
   print("=" * 50)
   print("SALES PERFORMANCE REPORT".center(50))
   print("=" * 50)
   print(f"Total orders        : {len(df)}")
   print(f"Completed orders    : {completed_orders}")
   print(f"Cancelled orders    : {cancelled_orders}")
   print(f"Returned orders     : {returned_orders}")
   print("-" * 50)
   print(f"Total revenue       : {total_rev_sum:,}")
   print(f"Average order value : {avg_order_val:,}")
   print("-" * 50)
   print(f"Top region          : {total_revenue.idxmax()}")
   print(f"Top product         : {total_product.idxmax()}")
   print(f"Top salesperson     : {top_salesperson.idxmax()}")
   print("-" * 50)
   print(f"Best payment mode   : {best_payment}")
   print("=" * 50)
   return df


with DAG(
        dag_id="sales_etl_pipeline",
        default_args=default_args,
        schedule_interval=None,
        start_date=datetime(2024, 1, 1),
        catchup=False,
        tags=["sales", "employees"],
) as dag:
   t1 = PythonOperator(task_id="extract", python_callable=extract)
   t2 = PythonOperator(task_id="clean", python_callable=clean)
   t3 = PythonOperator(task_id="transform", python_callable=transform)
   t4 = PythonOperator(task_id="analyse", python_callable=analyse)
   t1 >> t2 >> t3 >> t4