import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_100_servers():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    data = []
    now = datetime.now()
    
    for i in range(100):
        srv_id = f"srv-{i:03d}"
        for hour in range(24):
            ts = now - timedelta(hours=hour)
            # Power fluctuates with a base load + random noise
            power = 150 + np.random.uniform(50, 200)
            data.append({
                "server_id": srv_id,
                "timestamp": ts.isoformat(),
                "power_total_watts": power,
                "grid_intensity": np.random.uniform(100, 450),
                "inlet_temp_c": np.random.uniform(18, 32)
            })
            
    pd.DataFrame(data).to_csv("data/test_metrics.csv", index=False)
    print("Success: Generated 100-server data in data/test_metrics.csv")

if __name__ == "__main__":
    generate_100_servers()
