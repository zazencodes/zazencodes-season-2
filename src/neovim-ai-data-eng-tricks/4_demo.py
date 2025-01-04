import pyspark.sql.functions as F
from pyspark.sql import SparkSession

# Create Spark session with remote connection
spark = SparkSession.builder \
    .appName("DataTransformation") \
    .master("spark://spark-master:7077") \
    .config("spark.driver.memory", "2g") \
    .config("spark.executor.memory", "2g") \
    .getOrCreate()

# Sample dataset
df = spark.read.csv("data.csv", header=True)

# PySpark transformation
df = df.withColumn("age_category", F.when(F.col("age") < 30, "Young").otherwise("Old"))
df_filtered = df.filter(F.col("city") != "Chicago")
