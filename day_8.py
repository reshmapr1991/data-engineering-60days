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

spark = SparkSession.builder \
    .appName("UDF Practice") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# sample data
employees = spark.createDataFrame([
    ("E001", "Rahul Sharma",  90000),
    ("E002", "Priya Nair",    75000),
    ("E003", "Arjun Das",     85000),
    ("E004", "Sneha Iyer",    60000),
    ("E005", "Karan Singh",   95000),
    ("E006", "Meera Pillai",  70000),
    ("E007", "Vikram Gupta",  88000),
    ("E008", "Anjali Joshi",  62000),
], ["emp_id", "name", "salary"])

employees.show()

import os
os.environ["HADOOP_HOME"] = r"C:\Users\Public\PycharmProjects\hadoop"
os.environ["PATH"] += r";C:\Users\Public\PycharmProjects\hadoop\bin"

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, when, isnull, isnan, count, avg, sum,
    round, upper, lower, trim, lit, udf,
    broadcast, coalesce, regexp_replace
)
from pyspark.sql.types import (
    StringType, IntegerType, DoubleType, BooleanType
)
from pyspark.sql.window import Window
from pyspark.sql.functions import rank, dense_rank, lag, lead

spark = SparkSession.builder \
    .appName("Spark Advanced - Day 8") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("="*50)
print("DAY 8 — ADVANCED PYSPARK")
print("="*50)


# ── SECTION 1: Create sample DataFrames ──────────────────────────────────────

employees = spark.createDataFrame([
    ("E001", "Rahul Sharma",  "D001", 90000, "Delhi"),
    ("E002", "Priya Nair",    "D002", 75000, "Mumbai"),
    ("E003", "Arjun Das",     "D001", 85000, "Chennai"),
    ("E004", "Sneha Iyer",    "D003", 60000, "Bengaluru"),
    ("E005", "Karan Singh",   "D001", 95000, "Delhi"),
    ("E006", "Meera Pillai",  "D002", 70000, "Kochi"),
    ("E007", "Vikram Gupta",  "D001", 88000, "Hyderabad"),
    ("E008", "Anjali Joshi",  "D003", 62000, "Pune"),
    ("E009", "Rohit Babu",    "D002", 78000, "Bengaluru"),
    ("E010", "Divya Krishna", "D001", 82000, "Chennai"),
    ("E011", "Suresh Das",    "D004", 55000, "Delhi"),    # D004 has no dept record
    ("E012", "Kavya Menon",   None,   48000, "Mumbai"),  # NULL dept_id
], ["emp_id", "name", "dept_id", "salary", "city"])

departments = spark.createDataFrame([
    ("D001", "Engineering", "Amit Singh",  5000000),
    ("D002", "Marketing",   "Suresh Rao",  3000000),
    ("D003", "HR",          "Priya Menon", 1500000),
    ("D005", "Finance",     "Vikram Das",  2000000),  # no employees
], ["dept_id", "dept_name", "manager", "budget"])

print("Employees:")
employees.show()

print("Departments:")
departments.show()


# ── SECTION 2: JOINS ─────────────────────────────────────────────────────────
print("\n--- INNER JOIN ---")
# only matching rows from both tables
inner = employees.join(departments, on="dept_id", how="inner")
inner.select("name", "dept_name", "salary", "manager").show()
print(f"Inner join rows: {inner.count()}")  # E011(D004) and E012(None) excluded

print("\n--- LEFT JOIN ---")
# all employees, even if no department match
left = employees.join(departments, on="dept_id", how="left")
left.select("name", "dept_name", "salary").show()
print(f"Left join rows: {left.count()}")  # all 12 employees

print("\n--- RIGHT JOIN ---")
# all departments, even if no employees
right = employees.join(departments, on="dept_id", how="right")
right.select("name", "dept_name", "salary").show()
print(f"Right join rows: {right.count()}")  # Finance shows with null employee

print("\n--- FULL OUTER JOIN ---")
# everything from both sides
full = employees.join(departments, on="dept_id", how="full")
full.select("name", "dept_name", "salary").show()
print(f"Full outer join rows: {full.count()}")

print("\n--- BROADCAST JOIN ---")
# use when one table is small (fits in memory)
# Spark sends small table to ALL workers — avoids shuffle
# this is a HUGE performance optimization
broadcast_join = employees.join(
    broadcast(departments),  # broadcast the small departments table
    on="dept_id",
    how="inner"
)
broadcast_join.select("name", "dept_name", "salary").show()
print("Broadcast join — departments table sent to all workers")


# ── SECTION 3: Handling NULLs ────────────────────────────────────────────────
print("\n--- NULL HANDLING ---")

# create df with nulls
null_data = spark.createDataFrame([
    ("E001", "Rahul",  90000,  "Delhi"),
    ("E002", "Priya",  None,   "Mumbai"),   # null salary
    ("E003", None,     85000,  "Chennai"),  # null name
    ("E004", "Sneha",  60000,  None),       # null city
    ("E005", "Karan",  None,   None),       # multiple nulls
], ["emp_id", "name", "salary", "city"])

print("Data with nulls:")
null_data.show()

# count nulls per column
print("Null counts per column:")
null_data.select([
    count(when(col(c).isNull(), c)).alias(c)
    for c in null_data.columns
]).show()

# fill nulls
filled = null_data \
    .fillna({"salary": 0, "name": "Unknown", "city": "Not Specified"})
print("After filling nulls:")
filled.show()

# drop rows where ANY column is null
dropped = null_data.dropna()
print(f"After dropping nulls: {dropped.count()} rows")

# drop rows where SPECIFIC column is null
dropped_salary = null_data.dropna(subset=["salary"])
print(f"After dropping null salary: {dropped_salary.count()} rows")

# coalesce — use first non-null value
null_data2 = null_data.withColumn(
    "city_clean",
    coalesce(col("city"), lit("Bengaluru"))  # if city is null use Bengaluru
)
print("With coalesce:")
null_data2.show()


# ── SECTION 4: UDFs (User Defined Functions) ─────────────────────────────────
print("\n--- UDFs ---")

# UDF = custom Python function that runs on each row
# use when built-in Spark functions aren't enough

# define a Python function
def salary_grade(salary):
    if salary is None:
        return "Unknown"
    elif salary >= 90000:
        return "Grade A"
    elif salary >= 75000:
        return "Grade B"
    elif salary >= 60000:
        return "Grade C"
    else:
        return "Grade D"

# register as UDF
salary_grade_udf = udf(salary_grade, StringType())

# apply to DataFrame
graded = employees.withColumn(
    "grade",
    salary_grade_udf(col("salary"))
)
print("With salary grades:")
graded.select("name", "salary", "grade").show()

# UDF for string cleaning
def clean_name(name):
    if name is None:
        return None
    return name.strip().title()

clean_name_udf = udf(clean_name, StringType())

# apply string cleaning UDF
cleaned = employees.withColumn("clean_name", clean_name_udf(col("name")))
cleaned.select("name", "clean_name").show()

print("NOTE: UDFs are slower than built-in functions")
print("Always prefer built-in functions when possible")
print("Use UDFs only for complex custom logic")


# ── SECTION 5: WHEN / OTHERWISE (like CASE WHEN in SQL) ─────────────────────
print("\n--- WHEN / OTHERWISE ---")

# this is faster than UDF for simple conditions
employees_graded = employees.withColumn(
    "grade",
    when(col("salary") >= 90000, "Grade A")
    .when(col("salary") >= 75000, "Grade B")
    .when(col("salary") >= 60000, "Grade C")
    .otherwise("Grade D")
).withColumn(
    "above_avg",
    when(col("salary") > 78500, True).otherwise(False)
)

print("With WHEN/OTHERWISE:")
employees_graded.select(
    "name", "salary", "grade", "above_avg"
).show()


# ── SECTION 6: String operations ─────────────────────────────────────────────
print("\n--- STRING OPERATIONS ---")

employees.select(
    col("name"),
    upper(col("name")).alias("upper_name"),
    lower(col("name")).alias("lower_name"),
    trim(col("name")).alias("trimmed"),
    regexp_replace(col("name"), " ", "_").alias("underscored")
).show()


# ── SECTION 7: Partitioning ───────────────────────────────────────────────────
print("\n--- PARTITIONING ---")

# check current partitions
print(f"Default partitions: {employees.rdd.getNumPartitions()}")

# repartition — increase partitions (use for large data)
repartitioned = employees.repartition(4)
print(f"After repartition(4): {repartitioned.rdd.getNumPartitions()}")

# coalesce — decrease partitions (use before writing)
coalesced = employees.coalesce(1)
print(f"After coalesce(1): {coalesced.rdd.getNumPartitions()}")

# write partitioned by column — very common in DE
employees_graded.write \
    .mode("overwrite") \
    .partitionBy("grade") \
    .parquet("data/employees_partitioned")

print("Written partitioned by grade!")
print("Check data/employees_partitioned/ folder")
print("You'll see separate folders: grade=Grade A, grade=Grade B etc.")


# ── SECTION 8: Window functions ───────────────────────────────────────────────
print("\n--- WINDOW FUNCTIONS IN SPARK ---")

window_dept = Window.partitionBy("dept_id").orderBy(col("salary").desc())

windowed = employees.withColumn(
    "dept_rank", rank().over(window_dept)
).withColumn(
    "salary_lag", lag("salary", 1).over(window_dept)
).withColumn(
    "salary_diff", col("salary") - lag("salary", 1).over(window_dept)
)

print("Window functions result:")
windowed.select(
    "name", "dept_id", "salary", "dept_rank", "salary_lag", "salary_diff"
).orderBy("dept_id", "dept_rank").show()

spark.stop()
print("\nDay 8 Complete!")