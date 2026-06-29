from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys
import os

python_path = sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['HADOOP_HOME'] ="hadoop"
os.environ['JAVA_HOME'] = r''
######################🔴🔴🔴################################
conf = SparkConf().setAppName("pyspark").setMaster("local[*]").set("spark.driver.host","localhost").set("spark.default.parallelism", "1")
sc = SparkContext(conf=conf)

spark = SparkSession.builder.getOrCreate()

#print spark version
print("Spark version :",spark.version)
print("="*50)

#data
data = [
    ("E001", "Rahul Sharma",  "Engineering", 90000, "Delhi",     2019),
    ("E002", "Priya Nair",    "Marketing",   75000, "Mumbai",    2021),
    ("E003", "Arjun Das",     "Engineering", 85000, "Chennai",   2018),
    ("E004", "Sneha Iyer",    "HR",          60000, "Bengaluru", 2022),
    ("E005", "Karan Singh",   "Engineering", 95000, "Delhi",     2016),
    ("E006", "Meera Pillai",  "Marketing",   70000, "Kochi",     2023),
    ("E007", "Vikram Gupta",  "Engineering", 88000, "Hyderabad", 2018),
    ("E008", "Anjali Joshi",  "HR",          62000, "Pune",      2020),
    ("E009", "Rohit Babu",    "Marketing",   78000, "Bengaluru", 2015),
    ("E010", "Divya Krishna", "Engineering", 82000, "Chennai",   2022),
]

columns = ["emp_id", "name", "department", "salary", "city", "joining_year"]

df = spark.createDataFrame(data, columns)

# show the dataframe — this is an ACTION (triggers execution)
print("Full DataFrame:")
df.show()
# schema — like dtypes in pandas
print("Schema:")
df.printSchema()

# select specific columns — like SQL SELECT
print("Name and Salary only:")
df.select("name", "salary").show()

# filter — like SQL WHERE
print("Engineering employees:")
df.filter(df.department == "Engineering").show()

# filter with multiple conditions
print("Engineering + salary > 85000:")
df.filter(
    (df.department == "Engineering") & (df.salary > 85000)
).show()

# select specific columns — like SQL SELECT
print("Name and Salary only:")
df.select("name", "salary").show()

# filter — like SQL WHERE
print("Engineering employees:")
df.filter(df.department == "Engineering").show()

# filter with multiple conditions
print("Engineering + salary > 85000:")
df.filter(
    (df.department == "Engineering") & (df.salary > 85000)
).show()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, round

# ── STEP 1: Create SparkSession ───────────────────────────────────────────────
# SparkSession is the entry point to everything in Spark
# Think of it like a database connection object

spark = SparkSession.builder \
    .appName("DE Learning - Day 7") \
    .master("local[*]") \
    .getOrCreate()

# local[*] means run on your local machine using all CPU cores
# in production this would be a cluster address

print("Spark version:", spark.version)
print("="*50)


# ── STEP 2: Create a DataFrame ────────────────────────────────────────────────
# Just like pandas DataFrame but distributed

data = [
    ("E001", "Rahul Sharma",  "Engineering", 90000, "Delhi",     2019),
    ("E002", "Priya Nair",    "Marketing",   75000, "Mumbai",    2021),
    ("E003", "Arjun Das",     "Engineering", 85000, "Chennai",   2018),
    ("E004", "Sneha Iyer",    "HR",          60000, "Bengaluru", 2022),
    ("E005", "Karan Singh",   "Engineering", 95000, "Delhi",     2016),
    ("E006", "Meera Pillai",  "Marketing",   70000, "Kochi",     2023),
    ("E007", "Vikram Gupta",  "Engineering", 88000, "Hyderabad", 2018),
    ("E008", "Anjali Joshi",  "HR",          62000, "Pune",      2020),
    ("E009", "Rohit Babu",    "Marketing",   78000, "Bengaluru", 2015),
    ("E010", "Divya Krishna", "Engineering", 82000, "Chennai",   2022),
]

columns = ["emp_id", "name", "department", "salary", "city", "joining_year"]

df = spark.createDataFrame(data, columns)

# show the dataframe — this is an ACTION (triggers execution)
print("Full DataFrame:")
df.show()

# schema — like dtypes in pandas
print("Schema:")
df.printSchema()


# ── STEP 3: Basic operations ──────────────────────────────────────────────────

# select specific columns — like SQL SELECT
print("Name and Salary only:")
df.select("name", "salary").show()

# filter — like SQL WHERE
print("Engineering employees:")
df.filter(df.department == "Engineering").show()

# filter with multiple conditions
print("Engineering + salary > 85000:")
df.filter(
    (df.department == "Engineering") & (df.salary > 85000)
).show()

# ── STEP 4: groupBy + aggregations ───────────────────────────────────────────
# like SQL GROUP BY

print("Department stats:")
df.groupBy("department") \
  .agg(
      count("emp_id").alias("employee_count"),
      round(avg("salary"), 0).alias("avg_salary"),
      sum("salary").alias("total_salary")
  ).show()


# ── STEP 5: Adding new columns ────────────────────────────────────────────────
# withColumn — like pandas assign

df = df.withColumn("experience_years", 2024 - df.joining_year)
df = df.withColumn("salary_usd", round(df.salary / 83, 0))

print("With new columns:")
df.select("name", "salary", "experience_years", "salary_usd").show()


# ── STEP 6: orderBy ───────────────────────────────────────────────────────────
print("Top 5 earners:")
df.orderBy(df.salary.desc()).show(5)


# ── STEP 7: SQL on Spark DataFrames ──────────────────────────────────────────
# you can run actual SQL on Spark DataFrames!

# register as temp view
df.createOrReplaceTempView("employees")

# run SQL
result = spark.sql("""
    SELECT department,
           COUNT(*) as emp_count,
           ROUND(AVG(salary), 0) as avg_salary
    FROM employees
    GROUP BY department
    ORDER BY avg_salary DESC
""")

print("SQL on Spark:")
result.show()


# ── STEP 8: Pandas vs Spark comparison ───────────────────────────────────────
print("="*50)
print("Key differences from pandas:")
print("pandas  → df[df.salary > 80000]")
print("Spark   → df.filter(df.salary > 80000)")
print("")
print("pandas  → df.groupby().mean()")
print("Spark   → df.groupBy().agg(avg())")
print("")
print("pandas  → df['new_col'] = value")
print("Spark   → df.withColumn('new_col', value)")
print("="*50)


# ── always stop SparkSession at the end ──────────────────────────────────────
spark.stop()
print("SparkSession stopped.")