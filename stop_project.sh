#!/bin/bash

echo "🛑 Stopping GreenThinking Infrastructure..."

# 1. Stop and remove containers
docker compose down

# 2. Optional: Clean up temporary Spark logs or old CSVs
# Uncomment the line below if you want to clear old predictions every time you stop
# rm output/final_predictions/*.csv

echo "🧹 Infrastructure stopped and cleaned."