import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] = r"C:\Users\Public\PycharmProjects\hadoop\bin;" + os.environ.get("PATH", "")

from pyspark.sql import SparkSession
from pyspark.sql.functions import coalesce, col, lit

spark = SparkSession.builder \
    .appName("Coalesce Practice") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# ── MEANING 1: coalesce() for partitions ─────────────────────────────────────
data = spark.range(1000)  # 1000 rows
print(f"Default partitions: {data.rdd.getNumPartitions()}")

data4 = data.repartition(8)
print(f"After repartition(8): {data4.rdd.getNumPartitions()}")

data1 = data4.coalesce(2)
print(f"After coalesce(2): {data1.rdd.getNumPartitions()}")

# ── MEANING 2: coalesce() for null handling ───────────────────────────────────
employees = spark.createDataFrame([
    ("E001", "Rahul",  "Delhi",     "9876543210"),
    ("E002", "Priya",  None,        "9123456789"),  # null city
    ("E003", "Arjun",  "Chennai",   None),           # null phone
    ("E004", "Sneha",  None,        None),            # both null
    ("E005", "Karan",  "Delhi",     "9988776655"),
], ["emp_id", "name", "city", "phone"])

print("\nOriginal data with nulls:")
employees.show()

# coalesce(col, fallback) — use fallback if col is null
result = employees.withColumn(
    "city_clean",
    coalesce(col("city"), lit("City Not Available"))
).withColumn(
    "phone_clean",
    coalesce(col("phone"), lit("No Phone"))
)

print("After coalesce null handling:")
result.show()

# coalesce with multiple fallbacks — tries each one
# useful when you have backup columns
employees2 = spark.createDataFrame([
    ("E001", "Delhi",   None,      None),
    ("E002", None,      "Mumbai",  None),
    ("E003", None,      None,      "Chennai"),
    ("E004", None,      None,      None),
], ["emp_id", "primary_city", "secondary_city", "tertiary_city"])

print("Multiple fallback columns:")
employees2.withColumn(
    "best_city",
    coalesce(
        col("primary_city"),    # try this first
        col("secondary_city"),  # if null try this
        col("tertiary_city"),   # if null try this
        lit("Unknown")          # final fallback
    )
).show()

print("="*50)
print("COALESCE RULES:")
print("="*50)
print("df.coalesce(n)          → reduce partitions (no shuffle)")
print("coalesce(col, lit(val)) → null fallback (use val if null)")
print("coalesce(c1, c2, c3)    → try each column until non-null")

spark.stop()