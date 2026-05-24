import pandas as pd
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import glob

# Connection details (Matches your docker-compose)
token = "8UQhpkFFUhayrciEAnvRzEpobV1T6svqiZcu-dSAg7rfJu44ykeMwciJ9bmaofjHUDopZfbjTlisObPOTgLbdw=="
org = "green_it"  # If 'primary' doesn't work, we will check the org list below
bucket = "pollution_data"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Load the latest Spark output
files = glob.glob("output/final_predictions/*.csv")
for f in files:
    df = pd.read_csv(f)
    for _, row in df.iterrows():
        point = Point("server_metrics") \
            .tag("server_id", row['server_id']) \
            .field("actual_carbon", float(row['carbon_footprint'])) \
            .field("predicted_carbon", float(row['prediction'])) \
            .time(row['timestamp'])
        write_api.write(bucket=bucket, org=org, record=point)

print("Ingestion Complete!")