import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

# Set seed for reproducibility
np.random.seed(42)

# Parameters
n_users = 10000
start_date = datetime.now() - timedelta(days=30)

# Rates
control_cr = 0.120      # 12.0% conversion rate
treatment_cr = 0.138    # 13.8% conversion rate (~15% relative lift)

data = []
for i in range(1, n_users + 1):
    user_id = 100000 + i
    
    # Assign group (50/50 split)
    group = 'treatment' if np.random.rand() < 0.5 else 'control'
    landed_page = 'new_page' if group == 'treatment' else 'old_page'
    
    # Convert probability based on group
    cr = treatment_cr if group == 'treatment' else control_cr
    converted = 1 if np.random.rand() < cr else 0
    
    # Random device & location
    device = np.random.choice(['Desktop', 'Mobile', 'Tablet'], p=[0.50, 0.40, 0.10])
    location = np.random.choice(['Germany', 'France', 'UK', 'Spain', 'Italy'], p=[0.40, 0.20, 0.18, 0.12, 0.10])
    
    # Date spreads over 30 days
    rand_days = np.random.randint(0, 30)
    rand_hours = np.random.randint(0, 24)
    timestamp = (start_date + timedelta(days=rand_days, hours=rand_hours)).strftime('%Y-%m-%d %H:%M:%S')
    
    data.append([user_id, timestamp, group, landed_page, converted, device, location])

columns = ['user_id', 'timestamp', 'group', 'landed_page', 'converted', 'device', 'location']
df = pd.DataFrame(data, columns=columns)

# Sort by timestamp
df = df.sort_values('timestamp').reset_index(drop=True)

# Save to CSV
base_dir = r'C:\Users\anusu\.gemini\antigravity\scratch\analytics-portfolio\ab-test-conversion-analysis\data'
os.makedirs(base_dir, exist_ok=True)
output_path = os.path.join(base_dir, 'ab_test_data.csv')
df.to_csv(output_path, index=False)

print(f"Generated A/B test experiment data with {n_users} users at {output_path}")
