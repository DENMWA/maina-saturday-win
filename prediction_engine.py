import numpy as np
import pandas as pd
import joblib
from train_model import train_model

def generate_predictions(n_sets=50, strategy='blend'):
    numbers_pool = list(range(1, 46))
    predictions = []

    for i in range(n_sets):
        if strategy == 'hot':
            chosen = sorted(np.random.choice(numbers_pool[-20:], 6, replace=False))
        elif strategy == 'cold':
            chosen = sorted(np.random.choice(numbers_pool[:20], 6, replace=False))
        else:
            chosen = sorted(np.random.choice(numbers_pool, 6, replace=False))

        supplementaries = sorted(np.random.choice([x for x in numbers_pool if x not in chosen], 2, replace=False))
        predictions.append({
            "Main": chosen,
            "Supp": supplementaries
        })

    return predictions

def score_predictions(predictions):
    model = joblib.load("models/trained_rf_model.pkl")
    features = [p["Main"] + p["Supp"] for p in predictions]
    X = pd.DataFrame(features, columns=[f'N{i+1}' for i in range(8)])
    scores = model.predict_proba(X)[:, 1]
    for i, score in enumerate(scores):
        predictions[i]["Score"] = round(score, 4)
    return predictions

def update_historical_and_retrain(new_draw, historical_path="data/historical_draws.csv"):
    df = pd.read_csv(historical_path)
    new_entry = pd.DataFrame([new_draw], columns=[f'N{i+1}' for i in range(8)] + ['Win'])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(historical_path, index=False)
    train_model(historical_path)