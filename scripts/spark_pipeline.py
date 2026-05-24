from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, avg
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
import os

# Initialize Spark
spark = SparkSession.builder \
    .appName("GreenThinking_ML") \
    .getOrCreate()

# 1. Load Data
input_path = "/opt/project/data/test_metrics.csv"
df = spark.read.csv(input_path, header=True, inferSchema=True)

# 2. Green IT Logic: PUE & Carbon Footprint
# If temp > 25, cooling efficiency drops (PUE 1.3), otherwise 1.1
df = df.withColumn("pue", when(col("inlet_temp_c") > 25, 1.3).otherwise(1.1))

df = df.withColumn("carbon_footprint", 
    (col("power_total_watts") / 1000) * col("grid_intensity") * col("pue"))

# 3. Machine Learning: Random Forest
# Predict carbon footprint based on Power, Intensity, and Temp
assembler = VectorAssembler(
    inputCols=["power_total_watts", "grid_intensity", "inlet_temp_c"],
    outputCol="features"
)

ml_prep = assembler.transform(df)
rf = RandomForestRegressor(featuresCol="features", labelCol="carbon_footprint")
model = rf.fit(ml_prep)
predictions = model.transform(ml_prep)

# 4. Save Results
output_path = "/opt/project/output/final_predictions"
predictions.select("server_id", "timestamp", "carbon_footprint", "prediction") \
    .write.mode("overwrite").option("header", "true").csv(output_path)

print(f"Project Successful. Data written to: {output_path}")
spark.stop()