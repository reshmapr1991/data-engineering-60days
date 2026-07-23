from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

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
   print("csv read")

   #calculate revenue
   df["revenue"]=df["quantity"] * df["unit_price"]
   print(df["revenue"])

   #extract month from order_date
   df["order_date"]=pd.to_datetime(df["order_date"])
   df["month"]=df["order_date"].dt.month

   #filter completed orders
   filtered_df=df[df["status"] == "completed"]
   print(f"Filtered df:{filtered_df}")

   #save df
   df.to_csv(f"{DATA_DIR}/transform_csv.csv",index=False)
   print("Saved transform data")

def analyse():
   df=pd.read_csv(f"{DATA_DIR}/transform_csv.csv")

   #region has highest revenue
   total_revenue = df.groupby("region")["revenue"].sum()
   print(f"Region: {total_revenue.idxmax()}, Revenue: {total_revenue.max()}")

   #product sells the most by quantity
   total_product= df.groupby("product")["quantity"].sum()
   print(f"Product: {total_product.idxmax()}, Quantity: {total_product.max()}")

   #salesperson generated most revenue
   top_salesperson =df.groupby("salesperson")["revenue"].sum()
   top_salesperson_1 = top_salesperson.idxmax()
   highest_revenue = top_salesperson.max()
   print("Top salesperson:", top_salesperson_1)
   print("Revenue generated:", highest_revenue)

   #revenue split by payment mode
   revenue_split=df.groupby("payment_mode")["revenue"].sum().reset_index()
   print(revenue_split)

   #orders cancelled,returned and completed
   completed_orders=len(df[df["status"]=="completed"])
   print(f"Completed orders:{completed_orders}")
   returned_orders = len(df[df["status"] == "returned"])
   print(f"Returned orders:{returned_orders}")
   cancelled_orders = len(df[df["status"] == "cancelled"])
   print(f"Cancelled orders:{cancelled_orders}")

   #generate report
   print("=" * 50)
   print("SALES PERFORMANCE REPORT".center(10))
   print("=" * 50)
   print(f"Total orders :{len(df)}")
   print(f"Completed orders:{completed_orders}")
   print(f"Cancelled orders:{cancelled_orders}")
   print(f"Returned orders:{returned_orders}")
   print("-" * 50)
   total_revenue_sum = df["revenue"].sum()
   print(f"Total revenue:{total_revenue_sum:,}")
   avg_order_value = df["revenue"].mean().round(0)
   print(f"Average order value:{avg_order_value:,}")
   print("-" * 50)
   print(f"Top Region:{total_revenue.idxmax()}")
   print(f"Top Product:{total_product.idxmax()}")
   print(f"Top Salesperson:{top_salesperson_1 }")
   print("-" * 50)
   payment_mode=df["payment_mode"].value_counts()
   print(f"Best payment mode:{payment_mode}")
   print("=" *50)
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