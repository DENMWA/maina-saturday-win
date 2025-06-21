import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

def train_model(data_path="data/historical_draws.csv", model_path="models/trained_rf_model.pkl"):
    df = pd.read_csv(data_path)
    X = df[[f'N{i+1}' for i in range(8)]]
    y = df['Win']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, model_path)
    return True