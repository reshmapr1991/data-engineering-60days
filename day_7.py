import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] += r";C:\Users\Public\PycharmProjects\hadoop\bin"

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, round, count, sum
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from pyspark.sql.window import Window
from pyspark.sql.functions import rank

spark = SparkSession.builder \
    .appName("Spark File Operations") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ── READ CSV ──────────────────────────────────────────────────────────────────

schema = StructType([
    StructField("order_id",      StringType(),  True),
    StructField("customer_id",   StringType(),  True),
    StructField("customer_name", StringType(),  True),
    StructField("email",         StringType(),  True),
    StructField("city",          StringType(),  True),
    StructField("category",      StringType(),  True),
    StructField("product",       StringType(),  True),
    StructField("quantity",      IntegerType(), True),
    StructField("unit_price",    IntegerType(), True),
    StructField("order_date",    StringType(),  True),
    StructField("status",        StringType(),  True),
    StructField("valid_email",   StringType(),  True),
])

df = spark.read \
    .option("header", "true") \
    .schema(schema) \
    .csv("ecommerce_clean.csv")

print(f"Total rows: {df.count()}")
df.printSchema()
df.show(5)

# ── TRANSFORMATIONS ───────────────────────────────────────────────────────────
df = df.withColumn("revenue", col("quantity") * col("unit_price"))

# filter delivered only
delivered = df.filter(col("status") == "delivered")
print(f"\nDelivered orders: {delivered.count()}")

# revenue by category
print("\nRevenue by category:")
delivered.groupBy("category") \
    .agg(
        sum("revenue").alias("total_revenue"),
        count("order_id").alias("order_count"),
        round(avg("revenue"), 0).alias("avg_order_value")
    ) \
    .orderBy(col("total_revenue").desc()) \
    .show()

# revenue by city
print("\nRevenue by city:")
delivered.groupBy("city") \
    .agg(sum("revenue").alias("city_revenue")) \
    .orderBy(col("city_revenue").desc()) \
    .show()

# ── WINDOW FUNCTIONS ──────────────────────────────────────────────────────────
window = Window.partitionBy("category").orderBy(col("revenue").desc())
ranked = delivered.withColumn("rank_in_category", rank().over(window))

print("\nTop earner per category:")
ranked.filter(col("rank_in_category") == 1) \
      .select("customer_name", "category", "product", "revenue") \
      .show()

# ── WRITE PARQUET ─────────────────────────────────────────────────────────────
delivered.write \
    .mode("overwrite") \
    .parquet("data/delivered_orders.parquet")
print("\nSaved as Parquet!")

# read back
parquet_df = spark.read.parquet("data/delivered_orders.parquet")
print(f"Read back from Parquet: {parquet_df.count()} rows")

# ── SPARK SQL ─────────────────────────────────────────────────────────────────
df.createOrReplaceTempView("orders")

print("\nSpark SQL — status breakdown:")
spark.sql("""
    SELECT status,
           COUNT(*) as order_count,
           SUM(quantity * unit_price) as total_revenue
    FROM orders
    GROUP BY status
    ORDER BY total_revenue DESC
""").show()

spark.stop()
print("Done!")