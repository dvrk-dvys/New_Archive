from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("DeltaLakeExample") \
    .getOrCreate()

# Reading from a Delta table
df = spark.read.format("delta").load("/path/to/delta/table")

# Writing to a Delta table
df.write.format("delta").mode("overwrite").save("/path/to/delta/table")


#/path/to/delta/table/
#  part-00000-...-c000.snappy.parquet
#  part-00001-...-c000.snappy.parquet
#  _delta_log/
#    00000000000000000000.json
#    00000000000000000001.json
#    00000000000000000002.checkpoint.parquet

#Delta Lake:

#Data Files (.parquet): The actual data is stored in Parquet files.
#Each file represents a part of the table's data.
#Metadata Files (_delta_log/ directory): Delta Lake keeps a transaction log in the _delta_log/ directory.
#This log includes JSON files for each transaction that records data operations (like inserts, updates, and deletes)
#and Parquet files for checkpoints that provide a compact snapshot of the log's state.