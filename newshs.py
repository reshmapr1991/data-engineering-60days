from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys
import os
from pyspark.sql.functions import col, dense_rank
from pyspark.sql.window import Window

python_path = sys.executable
os.environ['PYSPARK_PYTHON'] = python_path
os.environ['HADOOP_HOME'] ="hadoop"
os.environ['JAVA_HOME'] = r''

conf = SparkConf().setAppName("pyspark").setMaster("local[*]").set("spark.driver.host","localhost").set("spark.default.parallelism", "1")
sc = SparkContext(conf=conf)

# Initialize Spark session (if not already done)
spark = SparkSession.builder.appName("SecondHighestSalary").getOrCreate()

#spark.read.format("csv").load("data/test.txt").toDF("Success").show(20, False)

# Sample data
data = [
    ("DEPT1", 1000),
    ("DEPT1", 700),
    ("DEPT1", 500),
    ("DEPT2", 400),
    ("DEPT2", 200),
    ("DEPT3", 500),
    ("DEPT3", 200)
]
columns = ["dept", "salary"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Define window specification
windowSpec = Window.partitionBy("dept").orderBy(col("salary").desc())

# Apply dense_rank()
ranked_df = df.withColumn("rank", dense_rank().over(windowSpec))

# Filter to get second highest salary (rank == 2)
second_highest_df = ranked_df.filter(col("rank") == 2)

# Show the result
second_highest_df.show()