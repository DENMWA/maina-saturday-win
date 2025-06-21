import streamlit as st
from prediction_engine import generate_predictions, score_predictions
import pandas as pd

st.title("Maina Saturday Win")
st.subheader("🔁 Adaptive Lotto Predictor with ML Scoring")

strategy = st.selectbox("Select Prediction Strategy", ["hot", "cold", "blend"])
if st.button("Generate Predictions"):
    raw_preds = generate_predictions(strategy=strategy)
    scored = score_predictions(raw_preds)
    df = pd.DataFrame([{
        **{f"N{i+1}": num for i, num in enumerate(p["Main"] + p["Supp"])},
        "Score": p["Score"]
    } for p in scored])
    st.dataframe(df)