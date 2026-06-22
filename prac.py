import pandas as pd
# df = pd.read_csv("claude.csv")
# print(df.shape)
# print(df.head())
# # How many duplicate order_ids exist?
# print(df.duplicated(subset=["order_id"]).sum())
# df = df.drop_duplicates(subset=["order_id"])
# print("After removing duplicates:", len(df))  # should be 30
# print(df['customer_name'].head(10))
# df["customer_name"] = df["customer_name"].str.strip().str.title()
# print(df['customer_name'])
# print(df[df['quantity']<=0])
# print(df[df['quantity']>0])
# print("After removing bad quantity:", len(df))
#
# print(df['email'])
# pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
# df['valid_email']=df['email'].str.match(pattern,na=False)
# print(df[df['valid_email'] ==False][["customer_name","email"]])
# df['revenue']=df["quantity"]* df["unit_price"]
# print(df[["product","unit_price","quantity","revenue"]].head())
# df['order_date']=pd.to_datetime(df["order_date"])
# print(df['order_date'].dtype)
# df["order_month"]=df["order_date"].dt.month
# print(df[["order_date","order_month"]].head())

#Load data
df = pd.read_csv("claude.csv")

#remove duplicates
df = df.drop_duplicates(subset=["order_id"])

#clean names
df["customer_name"] = df["customer_name"].str.strip().str.title()

#remove invalid quantity
print(df[df['quantity']>0])

#flag emails
pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
df['valid_email']=df['email'].str.match(pattern,na=False)

#revenue
df['revenue']=df["quantity"]* df["unit_price"]

#parse dates
df['order_date']=pd.to_datetime(df["order_date"])

df["order_month"]=df["order_date"].dt.month

print("\n Final shape:",df.shape)
print("\nNulCounts:",df.isnull().sum())
print("\nSample:",df.head())
df.to_csv("ecommerce_clean.csv",index=False)
print("\nSaved")

