import pandas as pd
import sys
import os

# Add src/ to the Python path manually
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from feature_extractor import extract_features  # Now direct import

# Load CSV
df = pd.read_csv("data/unlabeled_raw_leads.csv")
df_feat = extract_features(df)

# Print and save
print(df_feat.head())
df_feat.to_csv("data/processed_leads.csv", index=False)
print("Features extracted and saved.")
