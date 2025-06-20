# Maina Saturday Win (ML-Enhanced)

This version includes an integrated Random Forest machine learning model trained on Saturday Lotto historical draws.

## 🔍 Features
- Upload new results to auto-extend training data
- Auto re-trains model on updated dataset
- Scores new predictions using extracted statistical features
- Ranks predictions by Division 1–3 likelihood (proxy)

## 🔧 Structure
- `streamlit_app.py` - Upload interface and predictions
- `prediction_engine.py` - Extracts features + applies ML model
- `model_trainer.py` - Re-trains ML model with new historical data
- `data/` - Contains historical results
- `models/` - Stores trained model
