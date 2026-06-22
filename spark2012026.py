
from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col

# Create Spark session
spark = SparkSession.builder.appName("BigDataTask").getOrCreate()

path_to_file =  r"C:\Users\Public\PycharmProjects\file1.txt"

df = spark.read.format("csv") \
      .option("inferSchema", "true") \
      .load(path_to_file)
df = df.withColumnRenamed("_c0", "id") \
       .withColumnRenamed("_c1", "date") \
       .withColumnRenamed("_c2", "cid")\
       .withColumnRenamed("_c3", "time")\
       .withColumnRenamed("_c4", "sports")\
       .withColumnRenamed("_c5", "machines")\
       .withColumnRenamed("_c6", "Place")\
       .withColumnRenamed("_c7", "headquarters")\
       .withColumnRenamed("_c8", "cash_credit")

#Filter Exercise & Fitness

selected_df = df.select("id","cid","machines")
filtered_df = selected_df.filter(
   (col("sports")=="Exercise & Fitness" )|
   (col("machines")=="Cardio Machine")|
   (col("place")=="Columbus") |
   (col("headquarters")=="California")
)
splited_data =  selected_df.withColumn("machines",split(col("machines")," ")[0])
splited_data.show()


