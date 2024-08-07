from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .getOrCreate()

# Define the schema of the data
schema = StructType([
    StructField("user_id", StringType(), True),
    StructField("event", StringType(), True),
    StructField("amount", FloatType(), True)
])

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "ecommerce_events") \
    .load()

# Convert the data from JSON format
df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Perform some transformations
df_filtered = df.filter(col("event") == "purchase")

# Write the results to the console
query = df_filtered.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()


#Kafka is used for real-time data ingestion and streaming.
#-Producers send data to Kafka topics.
#-Brokers store and replicate the data.
#-Consumers read and process the data from Kafka topics.
#-Kafka can be integrated with Spark for real-time data processing, enabling powerful, low-latency data pipelines.