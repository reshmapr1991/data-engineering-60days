
from pyspark.sql import SparkSession
from pyspark.sql import *

spark = SparkSession.builder \
    .appName("MyApp") \
    .getOrCreate()



df = spark.createDataFrame(
     [(2, "Alice"), (5, "Bob")], ["age", "name"])
df.filter(df.name.rlike('ice$')).collect()
    [Row(age=2, name='Alice')]
print(df)
