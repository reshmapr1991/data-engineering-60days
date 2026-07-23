import boto3
import pandas as pd
from io import StringIO

# connect to S3
s3 = boto3.client("s3", region_name="ap-south-1")

BUCKET = "de-learning-reshma-2024"

# ── LIST FILES IN BUCKET ──────────────────────────────────────────────────────
print("Files in S3 bucket:")
response = s3.list_objects_v2(Bucket=BUCKET, Prefix="data/")
for obj in response["Contents"]:
    size_kb = obj["Size"] / 1024
    print(f"  {obj['Key']} ({size_kb:.1f} KB)")

# ── READ CSV FROM S3 INTO PANDAS ──────────────────────────────────────────────
print("\nReading sales_data.csv from S3...")
obj = s3.get_object(Bucket=BUCKET, Key="data/sales_data.csv")
df = pd.read_csv(obj["Body"])
print(f"Shape: {df.shape}")
print(df)

# ── PROCESS DATA ──────────────────────────────────────────────────────────────
print("\nProcessing data...")
df["revenue"] = df["quantity"] * df["price"]
df["city"] = df["city"].str.strip().str.title()

print("\nRevenue by city:")
city_revenue = df.groupby("city")["revenue"].sum().sort_values(ascending=False)
print(city_revenue)

print("\nTop product by quantity:")
top_product = df.groupby("product")["quantity"].sum().idxmax()
print(f"Top product: {top_product}")

# ── WRITE PROCESSED DATA BACK TO S3 ──────────────────────────────────────────
print("\nWriting processed data back to S3...")
csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=BUCKET,
    Key="processed/sales_processed.csv",
    Body=csv_buffer.getvalue()
)
print("Saved to s3://de-learning-reshma-2024/processed/sales_processed.csv")

# ── VERIFY ────────────────────────────────────────────────────────────────────
print("\nFiles in processed folder:")
response = s3.list_objects_v2(Bucket=BUCKET, Prefix="processed/")
for obj in response["Contents"]:
    print(f"  {obj['Key']}")

print("\nDone!")