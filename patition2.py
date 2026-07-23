import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] = r"C:\Users\Public\PycharmProjects\hadoop\bin;" + os.environ.get("PATH", "")

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys
import os

import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] = r"C:\Users\Public\PycharmProjects\hadoop\bin;" + os.environ.get("PATH", "")
python_path = sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['HADOOP_HOME'] ="hadoop"
os.environ['JAVA_HOME'] = r''
import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] = r"C:\Users\Public\PycharmProjects\hadoop\bin;" + os.environ.get("PATH", "")
######################🔴🔴🔴################################
conf = SparkConf().setAppName("pyspark").setMaster("local[*]").set("spark.driver.host","localhost").set("spark.default.parallelism", "1")
sc = SparkContext(conf=conf)

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, IntegerType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

spark = SparkSession.builder \
    .appName("Partitioning Practice") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# create sample data
employees = spark.createDataFrame([
    ("E001", "Rahul Sharma",  "Engineering", 90000),
    ("E002", "Priya Nair",    "Marketing",   75000),
    ("E003", "Arjun Das",     "Engineering", 85000),
    ("E004", "Sneha Iyer",    "HR",          60000),
    ("E005", "Karan Singh",   "Engineering", 95000),
    ("E006", "Meera Pillai",  "Marketing",   70000),
    ("E007", "Vikram Gupta",  "Engineering", 88000),
    ("E008", "Anjali Joshi",  "HR",          62000),
    ("E009", "Rohit Babu",    "Marketing",   78000),
    ("E010", "Divya Krishna", "Engineering", 82000),
], ["emp_id", "name", "department", "salary"])

# ── CHECK DEFAULT PARTITIONS ──────────────────────────────────────────────────
print(f"Default partitions: {employees.rdd.getNumPartitions()}")
# small data → 1 partition
# large data → Spark decides based on file size

# ── REPARTITION ───────────────────────────────────────────────────────────────
# increase partitions for parallel processing
big = employees.repartition(4)
print(f"After repartition(4): {big.rdd.getNumPartitions()}")
# now 4 workers can process simultaneously

# repartition by column — data with same dept goes to same partition
by_dept = employees.repartition(col("department"))
print(f"Repartitioned by department: {by_dept.rdd.getNumPartitions()}")
# all Engineering rows → partition 1
# all Marketing rows  → partition 2
# all HR rows         → partition 3
# this makes groupBy("department") much faster!

# ── COALESCE ──────────────────────────────────────────────────────────────────
# reduce partitions before writing
small = big.coalesce(1)
print(f"After coalesce(1): {small.rdd.getNumPartitions()}")
# 1 partition = 1 output file
# good for small datasets

# ── PARTITIONBY WHEN WRITING ──────────────────────────────────────────────────
# add grade column first
employees_graded = employees.withColumn(
    "grade",
    when(col("salary") >= 90000, "Grade_A")
    .when(col("salary") >= 75000, "Grade_B")
    .when(col("salary") >= 60000, "Grade_C")
    .otherwise("Grade_D")
)

# write partitioned by department
employees_graded.write \
    .mode("overwrite") \
    .partitionBy("department") \
    .csv("data/employees_by_dept")

print("\nWritten partitioned by department!")
print("Folder structure created:")
print("  data/employees_by_dept/")
print("  ├── department=Engineering/")
print("  ├── department=HR/")
print("  └── department=Marketing/")

# read only Engineering — Spark reads only that folder
eng_only = spark.read \
    .option("header", "false") \
    .csv("data/employees_by_dept/department=Engineering")
print(f"\nEngineering employees read: {eng_only.count()}")

# write partitioned by multiple columns
employees_graded.write \
    .mode("overwrite") \
    .partitionBy("department", "grade") \
    .csv("data/employees_by_dept_grade")

print("\nWritten partitioned by department + grade!")
print("Folder structure:")
print("  data/employees_by_dept_grade/")
print("  ├── department=Engineering/")
print("  │   ├── grade=Grade_A/")
print("  │   └── grade=Grade_B/")
print("  ├── department=HR/")
print("  │   └── grade=Grade_C/")
print("  └── department=Marketing/")

# ── WHEN TO USE WHAT ──────────────────────────────────────────────────────────
print("\n" + "="*50)
print("PARTITIONING RULES:")
print("="*50)
print("repartition(n)     → before heavy joins/groupBy")
print("repartition(col)   → when you groupBy same column")
print("coalesce(1)        → before writing small output")
print("partitionBy(col)   → when writing to data lake")
print("                     for partition pruning benefit")

spark.stop()