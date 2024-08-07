from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergExample") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .getOrCreate()

# Reading from an Iceberg table
df = spark.read.format("iceberg").load("db_name.table_name")

# Writing to an Iceberg table
df.write.format("iceberg").mode("overwrite").save("db_name.table_name")



#Apache Iceberg:

#Data Files (.parquet): Like Delta Lake, Iceberg stores its data in Parquet files. Each Parquet file is a chunk of the table's data.
#Metadata Files:
#Metadata JSON Files (.json): These files contain table-level metadata, such as schema, partition information, and snapshots.
#Manifest Files (.avro): Iceberg uses Avro files to store metadata about the data files, such as file paths, file sizes, and row counts. These are referred to as manifest lists.


#:Update Example:

spark = SparkSession.builder \
    .appName("IcebergExample") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .getOrCreate()


# Define the schema for the table
schema = "id INT, name STRING, age INT"

# Create an Iceberg table
spark.sql(f"""
CREATE TABLE spark_catalog.default.iceberg_table ({schema})
USING iceberg
""")

# Add new data to the Iceberg table
data = [(1, 'Alice', 30), (2, 'Bob', 25)]
df = spark.createDataFrame(data, schema.split(", "))

# Write data to the Iceberg table
df.writeTo("spark_catalog.default.iceberg_table").append()


# Update data in the Iceberg table
spark.sql("""
MERGE INTO spark_catalog.default.iceberg_table AS target
USING (SELECT 1 AS id, 'Alice' AS name, 35 AS age) AS source
ON target.id = source.id
WHEN MATCHED THEN
  UPDATE SET target.age = source.age
WHEN NOT MATCHED THEN
  INSERT (id, name, age) VALUES (source.id, source.name, source.age)
""")

#Updating Data
#When updating existing data in an Iceberg table:

#-Identify Affected Files: Iceberg identifies the specific Parquet files that contain the data to be updated.
#-Modify Data: The data in these Parquet files is updated or new Parquet files are created with the updated data.
#-Update Metadata: Iceberg updates its metadata to point to the new or modified Parquet files.
#-Commit Transaction: The updates are committed, and the old Parquet files can be removed or archived as needed.


from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("IcebergPartitioningExample") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkSessionCatalog") \
    .config("spark.sql.catalog.spark_catalog.type", "hive") \
    .getOrCreate()


# Define the schema for the table
schema = """
    deviceisbot BOOLEAN,
    screensize STRING,
    published STRING,
    type STRING,
    devicetype STRING,
    useragent STRING,
    objecttype STRING,
    eventname STRING,
    timedelta STRING,
    viewportsize STRING
"""
# Create an Iceberg table with partitioning by eventname
spark.sql(f"""
CREATE TABLE spark_catalog.default.recommendation_events ({schema})
USING iceberg
PARTITIONED BY (eventname)
""")

# Create a DataFrame with the example data
data = [
    (False, '1080x2401', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'RecommendationList', 'Recommendation widget impression', '0:00:00', 'Null'),
    (False, '1080x2150', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'Conversation', 'Conversation View', '0:00:00', 'Null'),
    (False, '720x1184', 'Request', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'MessageTemplate', 'Request template', '0:00:00', 'Null'),
    (False, '1170x2532', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'RecommendationList', 'Recommendation widget impression', '0:00:08', 'Null'),
    (False, '640x1136', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'RecommendationList', 'Recommendation widget impression', '0:00:00', 'Null'),
    (False, '1080x2153', 'Request', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'MessageTemplate', 'Request template', '0:00:00', 'Null'),
    (False, '1080x2330', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'RecommendationList', 'Recommendation widget impression', '0:00:00', 'Null'),
    (False, '720x1370', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'Conversation', 'Conversation View', '0:00:00', 'Null'),
    (False, '1170x2532', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'RecommendationList', 'Recommendation widget impression', '0:00:06', 'Null'),
    (False, '1125x2436', 'Request', 'mobile', 'iOSSPTTracker1.0.1', 'MessageTemplate', 'Request template', '0:00:00', 'Null'),
    (False, '720x1515', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'ConversationList', 'Inbox View', '0:00:00', 'Null'),
    (False, '1080x2190', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'MessageTemplate', 'Show template', '0:00:00', 'Null'),
    (False, '1125x2436', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'ConversationList', 'Inbox view', '0:00:00', 'Null'),
    (False, '720x1358', 'Click', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'RecommendationItem', 'Click on Last Search Widget', '0:00:00', 'Null'),
    (False, '1170x2532', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'MessageTemplate', 'Show template', '0:00:00', 'Null'),
    (False, '750x1334', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'UIElement', 'Show integration call to action', '0:00:00', 'Null'),
    (False, '1080x2110', 'Close', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'Conversation', 'Conversation Close', '0:00:00', 'Null'),
    (False, '1080x2144', 'Request', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'MessageTemplate', 'Request template', '0:00:00', 'Null'),
    (False, '1125x2436', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'UIElement', 'Show integration call to action', '0:00:09', 'Null'),
    (False, '1080x2134', 'View', 'mobile', 'Android-Pulse-Tracker/8.0.1', 'Conversation', 'Conversation View', '0:00:00', 'Null'),
    (False, '640x1136', 'View', 'mobile', 'iOSSPTTracker1.0.1', 'ConversationList', 'Inbox view', '0:00:00', 'Null')
]

df = spark.createDataFrame(data, schema.split(", "))

# Filter the DataFrame to include only recommendation widget impression events
recommendation_df = df.filter(df.eventname == 'Recommendation widget impression')

# Write data to the Iceberg table
recommendation_df.writeTo("spark_catalog.default.recommendation_events").append()


