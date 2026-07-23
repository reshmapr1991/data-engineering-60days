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
from pyspark.sql.functions import col, udf, when
from pyspark.sql.types import StringType, IntegerType, BooleanType, DoubleType

spark = SparkSession.builder \
    .appName("UDF Deep Dive") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

employees = spark.createDataFrame([
    ("E001", "rahul sharma",  90000, "9876543210", "Delhi"),
    ("E002", "  PRIYA NAIR",  75000, "9123456789", "Mumbai"),
    ("E003", "arjun das",     85000, "invalid",    "Chennai"),
    ("E004", "sneha iyer",    60000, "9988776655", "Bengaluru"),
    ("E005", "KARAN SINGH",   95000, "9871234567", "Delhi"),
    ("E006", "meera pillai",  70000, "abcdefghij", "Kochi"),
], ["emp_id", "name", "salary", "phone", "city"])

print("Original data:")
employees.show()

# ── WAY 1: Standard UDF ───────────────────────────────────────────────────────
print("--- Way 1: Standard UDF ---")

def clean_name(name):
    if name is None:
        return "Unknown"
    return name.strip().title()

clean_name_udf = udf(clean_name, StringType())
result1 = employees.withColumn("clean_name", clean_name_udf(col("name")))
result1.select("name", "clean_name").show()

# ── WAY 2: Lambda UDF ─────────────────────────────────────────────────────────
print("--- Way 2: Lambda UDF ---")

# simple one-liner → use lambda
salary_inr = udf(lambda s: f"₹{s:,}" if s else "N/A", StringType())
result2 = employees.withColumn("salary_formatted", salary_inr(col("salary")))
result2.select("name", "salary", "salary_formatted").show()

# ── WAY 3: Decorator UDF ──────────────────────────────────────────────────────
print("--- Way 3: Decorator UDF ---")

@udf(returnType=StringType())
def grade_udf(salary):
    if salary is None:
        return "Unknown"
    if salary >= 90000: return "Grade A"
    if salary >= 75000: return "Grade B"
    if salary >= 60000: return "Grade C"
    return "Grade D"

result3 = employees.withColumn("grade", grade_udf(col("salary")))
result3.select("name", "salary", "grade").show()

# ── REAL WORLD UDF: Phone validator ───────────────────────────────────────────
print("--- Real World: Phone Validator ---")

def validate_phone(phone):
    if phone is None:
        return False
    # valid Indian phone: 10 digits, starts with 6-9
    cleaned = phone.strip()
    if len(cleaned) == 10 and cleaned.isdigit():
        if cleaned[0] in ['6', '7', '8', '9']:
            return True
    return False

validate_phone_udf = udf(validate_phone, BooleanType())

phone_result = employees \
    .withColumn("phone_valid", validate_phone_udf(col("phone")))

phone_result.select("name", "phone", "phone_valid").show()

# ── REAL WORLD UDF: Tax calculator ────────────────────────────────────────────
print("--- Real World: Tax Calculator ---")


def calculate_tax(monthly_salary):
    if monthly_salary is None:
        return 0.0

    # convert monthly to annual
    annual = monthly_salary * 12

    # Indian income tax slabs on annual income
    if annual <= 250000:
        return 0.0
    elif annual <= 500000:
        return (annual - 250000) * 0.05
    elif annual <= 1000000:
        return 12500 + (annual - 500000) * 0.20
    else:
        return 112500 + (annual - 1000000) * 0.30
calculate_tax_udf = udf(calculate_tax, DoubleType())

tax_result = employees \
    .withColumn("annual_salary", col("salary") * 12) \
    .withColumn("annual_tax",
                calculate_tax_udf(col("salary"))) \
    .withColumn("monthly_tax",
                (calculate_tax_udf(col("salary")) / 12)) \
    .withColumn("in_hand_monthly",
                ((col("annual_salary") - calculate_tax_udf(col("salary"))) / 12))

tax_result.select(
    "name", "salary", "annual_salary", "annual_tax",
    "monthly_tax", "in_hand_monthly"
).show()
# ── UDF vs WHEN comparison ────────────────────────────────────────────────────
print("--- UDF vs WHEN/OTHERWISE ---")
print("Same result, different performance:\n")

# UDF approach
result_udf = employees.withColumn("grade_udf", grade_udf(col("salary")))

# WHEN approach (faster)
result_when = employees.withColumn(
    "grade_when",
    when(col("salary") >= 90000, "Grade A")
    .when(col("salary") >= 75000, "Grade B")
    .when(col("salary") >= 60000, "Grade C")
    .otherwise("Grade D")
)

result_udf.select("name", "salary", "grade_udf").show()
result_when.select("name", "salary", "grade_when").show()

print("="*50)
print("UDF RULES TO REMEMBER:")
print("="*50)
print("1. Always handle None/null inside UDF")
print("2. Always specify return type")
print("3. Use @udf decorator for clean syntax")
print("4. Use lambda for simple one-liners")
print("5. Prefer when/otherwise for simple conditions")
print("6. Use UDF for complex logic, validation,")
print("   external libraries, multi-step processing")

spark.stop()
print("UDF deep dive complete!")