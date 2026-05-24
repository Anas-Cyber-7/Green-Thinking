#!/bin/bash

echo "🚀 Starting GreenThinking Infrastructure..."
docker compose up -d
sleep 60

# 1. CLEAN OLD DATA (This ensures quality)
echo "🧹 Cleaning old records..."
rm -f data/*.csv
rm -f output/final_predictions/*.csv

# 2. Activate Virtual Environment
source .venv/bin/activate

# 3. RUN PIPELINE
echo "📊 Generating NEW Data..."
python3 data_generator.py

echo "🧠 Running Spark AI Pipeline..."
docker exec spark-master /spark/bin/spark-submit /opt/project/scripts/spark_pipeline.py

echo "📤 Ingesting results to InfluxDB..."
python3 scripts/ingest_to_influx.py

echo "✅ Success! View your fresh results at http://localhost:3000"
