import pandas as pd
import joblib

# Load model once
model = joblib.load("models/trust_model.pkl")

# Features used during training
FEATURE_COLUMNS = ['EmailLength', 'WebsiteHTTPS', 'MissingFields', 'HasDisposableDomain', 'EmailCompanyMatch']

def score_leads(df):
    df = df.copy()

    # Predict trust probability (0–1), scale to 0–100
    df['TrustScore'] = model.predict_proba(df[FEATURE_COLUMNS])[:, 1] * 100

    # Labeling based on score
    def label(score):
        if score >= 80:
            return "High Trust"
        elif score >= 50:
            return "Moderate Trust"
        else:
            return "Low Trust"

    df['TrustLevel'] = df['TrustScore'].apply(label)
    return df
