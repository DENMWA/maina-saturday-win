
import numpy as np
import pandas as pd
import joblib

# Load trained model
model = joblib.load("models/trained_rf_model.pkl")

# Load frequency for feature generation
def get_frequency_map(historical_file="data/Cleaned_Saturday_Historical.csv"):
    hist_df = pd.read_csv(historical_file)
    flat = pd.to_numeric(hist_df[['Main 1', 'Main 2', 'Main 3', 'Main 4', 'Main 5', 'Main 6']].values.flatten(), errors='coerce')
    return pd.Series(flat).value_counts()

freq_map = get_frequency_map()
hot_list = freq_map.sort_values(ascending=False).head(10).index.tolist()
cold_list = freq_map.sort_values().head(10).index.tolist()

# Extract features for a prediction set
def extract_features(mains):
    hot_count = sum(n in hot_list for n in mains)
    cold_count = sum(n in cold_list for n in mains)
    odd_count = sum(n % 2 != 0 for n in mains)
    even_count = 6 - odd_count
    spread = max(mains) - min(mains)
    mod_3 = sum(n % 3 == 0 for n in mains)
    avg_freq = sum(freq_map.get(n, 0) for n in mains) / 6
    return [hot_count, cold_count, odd_count, even_count, spread, mod_3, avg_freq]

# Score a DataFrame of predictions
def score_predictions(df):
    features = df['Main Numbers'].apply(lambda x: extract_features(eval(x))).tolist()
    probs = model.predict_proba(features)[:, 1]  # Probability of class 1
    df['Score'] = probs
    return df.sort_values(by='Score', ascending=False)
