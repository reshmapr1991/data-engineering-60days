import pandas as pd


DATA_DIR =r"C:\Users\Public\PycharmProjects\airflow_practice\dags\data"
def extract():

   df =pd.read_csv(f"{DATA_DIR}/sales.csv")
   # print table
   print(df)

   # print first 5 rows
   print(f"Head: {df.head()}")

   # print shape
   print(f"Shape:{df.shape}")

   # null counts
   print(f"Null count: {df.isnull().sum().sum()}")

   df.to_csv(f"{DATA_DIR}/sales_extracted.csv")
   print("Saved Extracted csv")

   return df

def clean():

   df = pd.read_csv(f"{DATA_DIR}/sales_extracted.csv")
   df["salesperson"] =df["salesperson"].str.strip().str.title()

   df = df[df["quantity"] > 0]
   df["quantity"]=df["quantity"].fillna(df["quantity"].median())

   df.to_csv(f"{DATA_DIR}/sales_cleaned.csv")
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
   filtered_df=(df.loc[df["status"]=="completed"])
   print(f"Filtered df:{filtered_df}")

   #save df
   df.to_csv(f"{DATA_DIR}/transform_csv.csv")
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
   revenue_sum=df["revenue"].sum()
   print(f"Total revenue:{revenue_sum}")
   avg_order_value=revenue_sum.mean()
   print(f"Average order value:{avg_order_value}")
   print("-" * 50)
   print(f"Top Region:{total_revenue.idxmax()}")
   print(f"Top Product:{total_product.idxmax()}")
   print(f"Top Salesperson:{top_salesperson_1 }")
   print("-" * 50)
   payment_mode=df["payment_mode"].value_counts()
   print(f"Best payment mode:{payment_mode}")
   print("=" *50)
   return df



if __name__ == "__main__":

  extract()
  clean()
  transform()
  analyse()