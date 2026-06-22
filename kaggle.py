
from pyspark.context import SparkContext
from pyspark.sql.session import SparkSession
sc = SparkContext('local')
spark = SparkSession(sc)
path = "C:/Users/TEJAS TOURS &TRAVELS/OneDrive/Desktop/kagglecsv.csv"
df = spark.read.option("header", True).option("multiLine", value = True).csv(path)
df.show()