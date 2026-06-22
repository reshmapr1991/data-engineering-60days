from pyspark.sql.functions import *


kinesisdf = (

              spark
              .readStream
              .format("aws-kinesis")
              .option("kinesis.streamName","UNIQUENAME")
              .option("kinesis.endpointUrl","https://kinesis.ap-south-1.amazonaws.com")
              .option("kinesis.startingposition","TRIM_HORIZON")
              .load()
              .withColumn("data",expr("cast(data as string)"))
              .select("data")

)


kinesisdf.writeStream.format("console").start().awaitTermination()